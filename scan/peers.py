import concurrent.futures
import logging
import random
import socket
from datetime import timedelta
from functools import lru_cache
from urllib.parse import urlparse

import requests
from cache_memoize import cache_memoize
from django import forms
from django.conf import settings
from django.db import transaction
from django.db.models import F, DurationField, ExpressionWrapper
from django.db.models.functions import Now
from django.utils import timezone
from requests.exceptions import RequestException
from sentry_sdk import capture_message

from java_wallet.models import Block
from burst.api.brs.p2p import P2PApi
from burst.api.exceptions import BurstException
from scan.decorators import lock_decorator
from scan.models import PeerMonitor


logger = logging.getLogger(__name__)


def get_ip_by_domain(peer: str) -> str or None:
    # truncating port if exists
    if not peer.startswith('http'):
        peer = 'http://{}'.format(peer)
    hostname = urlparse(peer).hostname

    if not hostname:
        return None

    # ipv6
    if ':' in hostname:
        return hostname

    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        logger.debug("Can't resolve host: %s - %r", peer, e)
        return None


@cache_memoize(60*60*24*7)
def get_country_by_ip(ip: str) -> str:
    try:
        response = requests.get('http://www.geoplugin.net/json.gp?ip={}'.format(ip))
        response.raise_for_status()
        json_response = response.json()
        return json_response['geoplugin_countryCode'] or '??'
    except (RequestException, ValueError, KeyError):
        return '??'


class PeerMonitorForm(forms.ModelForm):
    class Meta:
        model = PeerMonitor
        fields = '__all__'


def is_good_version(version: str) -> bool:
    m_major, m_minor, m_patch = settings.MIN_PEER_VERSION.split('.')

    version = version.replace('v', '')
    try:
        major, minor, patch = version.split('.')
        if int(major) < int(m_major):
            return False
        if int(minor) < int(m_minor):
            return False
        return True
    except ValueError:
        return False


@lru_cache(maxsize=None)
def get_last_cumulative_difficulty() -> dict:
    result = Block.objects.using('java_wallet').order_by(
        '-height'
    ).values(
        'height', 'cumulative_difficulty'
    ).first()

    result['cumulative_difficulty'] = str(int(result['cumulative_difficulty'].hex(), 16))

    return result


@lru_cache(maxsize=None)
def get_block_cumulative_difficulty(height: int) -> str:
    cumulative_difficulty = Block.objects.using('java_wallet').filter(
        height=height
    ).values_list(
        'cumulative_difficulty', flat=True
    ).first()
    return str(int(cumulative_difficulty.hex(), 16))


def explore_peer(address: str, updates: dict):
    logger.debug('Peer: %s', address)

    if address in updates:
        return

    try:
        peer_info = P2PApi(address).get_info()
        if not is_good_version(peer_info['version']):
            logger.debug("Old version: %s", peer_info['version'])
            updates[address] = None
            return
        peer_info.update(P2PApi(address).get_cumulative_difficulty())
    except BurstException:
        logger.debug("Can't connect to peer: %s", address)
        updates[address] = None
        return

    ip = get_ip_by_domain(address)

    updates[address] = {
        'announced_address': peer_info['announcedAddress'],
        'country_code': get_country_by_ip(ip) if ip else '??',
        'application': peer_info['application'],
        'platform': peer_info['platform'],
        'version': peer_info['version'],
        'height': peer_info['blockchainHeight'],
        'cumulative_difficulty': peer_info['cumulativeDifficulty'],
        'last_online_at': timezone.now(),
    }


def explore_node(address: str, updates: dict):
    logger.debug('Node: %s', address)

    try:
        peers = P2PApi(address).get_peers()
        explore_peer(address, updates)
    except BurstException:
        logger.debug("Can't connect to node: %s", address)
        return

    if settings.TEST_NET:
        for peer in peers:
            explore_peer(peer, updates)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda p: explore_peer(p, updates), peers)


def get_nodes_list() -> list:
    # first check UNREACHABLE because more chance they are still offline
    # and timeout connection in worker
    addresses_offline = list(PeerMonitor.objects.values_list(
        'announced_address', flat=True
    ).filter(
        state=PeerMonitor.State.UNREACHABLE
    ).distinct()) or []

    # get other addresses exclude UNREACHABLE
    addresses_other = list(PeerMonitor.objects.values_list(
        'announced_address', flat=True
    ).exclude(
        state=PeerMonitor.State.UNREACHABLE
    ).distinct()) or []

    # add well-known peers
    addresses_other.extend(settings.BRS_BOOTSTRAP_PEERS)

    # mix it
    random.shuffle(addresses_offline)
    random.shuffle(addresses_other)

    # first UNREACHABLE
    return addresses_offline + addresses_other


def get_state(update: dict, peer_obj: PeerMonitor or None) -> int:
    _data = get_last_cumulative_difficulty()

    if update['height'] == _data['height']:
        if update['cumulative_difficulty'] == _data['cumulative_difficulty']:
            state = PeerMonitor.State.ONLINE
        else:
            state = PeerMonitor.State.FORKED
    elif update['height'] > _data['height']:
        state = PeerMonitor.State.FORKED
    else:
        if peer_obj and peer_obj.height == update['height']:
            state = PeerMonitor.State.STUCK
        else:
            _cumulative_difficulty = get_block_cumulative_difficulty(update['height'])
            if update['cumulative_difficulty'] == _cumulative_difficulty:
                state = PeerMonitor.State.SYNC
            else:
                state = PeerMonitor.State.FORKED

    return state


def get_count_nodes_online() -> int:
    return PeerMonitor.objects.filter(
        state=PeerMonitor.State.ONLINE
    ).count()


@lock_decorator(key='peer_monitor', expire=60, auto_renewal=True)
@transaction.atomic
def peer_cmd():
    logger.info('Start')

    addresses = get_nodes_list()

    # explore every peer and collect updates
    updates = {}
    if settings.TEST_NET:
        for address in addresses:
            explore_node(address, updates)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(lambda address: explore_node(address, updates), addresses)

    # if more than __% peers were gone offline in __min, probably network problem
    if len(updates) < get_count_nodes_online() * 0.9:
        logger.warning('Peers update was rejected: %d - %d', len(updates), len(addresses))
        capture_message('Peers update was rejected.')
        return

    # set all peers unreachable, if will no update - peer will be unreachable
    PeerMonitor.objects.update(state=PeerMonitor.State.UNREACHABLE)

    # calculate state and apply updates
    for update in updates.values():
        if not update:
            continue

        logger.debug('Update: %r', update)

        peer_obj = PeerMonitor.objects.filter(announced_address=update['announced_address']).first()
        if not peer_obj:
            logger.info('Found new peer: %s', update['announced_address'])

        update['state'] = get_state(update, peer_obj)

        form = PeerMonitorForm(update, instance=peer_obj)

        if form.is_valid():
            form.save()
        else:
            logger.info('Not valid data: %r - %r', form.errors, update)

    PeerMonitor.objects.update(lifetime=F('lifetime') + 1)

    PeerMonitor.objects.filter(
        state__in=[
            PeerMonitor.State.UNREACHABLE,
            PeerMonitor.State.STUCK,
        ]
    ).update(downtime=F('downtime') + 1)

    PeerMonitor.objects.annotate(
        duration=ExpressionWrapper(
            Now() - F('last_online_at'),
            output_field=DurationField())
    ).filter(
        duration__gte=timedelta(days=30)
    ).delete()

    PeerMonitor.objects.update(
        availability=100 - (F('downtime') / F('lifetime') * 100),
        modified_at=timezone.now()
    )
    logger.info('Done')
