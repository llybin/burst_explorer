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

from java_wallet.models import Block
from burst.api.brs.p2p import P2PApi
from burst.api.exceptions import BurstException
from scan.decorators import lock_decorator
from scan.models import PeerMonitor


logger = logging.getLogger(__name__)


@cache_memoize(60*60*24*7)
def get_country_by_ip(ip: str) -> str:
    try:
        response = requests.get('http://www.geoplugin.net/json.gp?ip={}'.format(ip))
        response.raise_for_status()
        json_response = response.json()
        return json_response['geoplugin_countryCode'] or '??'
    except (RequestException, ValueError, KeyError):
        return '??'


@lru_cache(maxsize=None)
def get_host_by_name(peer: str) -> str or None:
    # truncating port if exists
    if not peer.startswith('http'):
        peer = 'http://{}'.format(peer)
    hostname = urlparse(peer).hostname

    # ipv6
    if ':' in hostname:
        return hostname

    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as e:
        logger.debug("Can't resolve host: %s - %r", peer, e)
        return None


class PeerMonitorForm(forms.ModelForm):
    class Meta:
        model = PeerMonitor
        fields = '__all__'


def is_good_version(version: str) -> bool:
    version = version.replace('v', '')
    try:
        major, minor, patch = version.split('.')
        if int(major) < 2:
            return False
        if int(minor) < 3:
            return False
        return True
    except ValueError:
        return False


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

    ip = get_host_by_name(address)
    if not ip:
        return

    if ip in updates:
        return

    try:
        peer_info = P2PApi(address).get_info()
        if not is_good_version(peer_info['version']):
            logger.debug("Old version: %s", peer_info['version'])
            updates[ip] = None
            return
        peer_info.update(P2PApi(address).get_cumulative_difficulty())
    except BurstException:
        logger.debug("Can't connect to peer: %s", address)
        updates[ip] = None
        return

    updates[ip] = {
        '_data': get_last_cumulative_difficulty(),
        'ip': ip,
        'country_code': get_country_by_ip(ip),
        'announced_address': peer_info['announcedAddress'],
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

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(lambda peer: explore_peer(peer, updates), peers)


def get_nodes_list() -> list:
    # first check UNREACHABLE because more chance they are still offline
    # and 2 sec timeout connection in worker
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


def set_state(update: dict, peer_obj: PeerMonitor):
    if update['height'] == update['_data']['height']:
        if update['cumulative_difficulty'] == update['_data']['cumulative_difficulty']:
            update['state'] = PeerMonitor.State.ONLINE
        else:
            update['state'] = PeerMonitor.State.FORKED
    elif update['height'] > update['_data']['height']:
        update['state'] = PeerMonitor.State.FORKED
    else:
        if peer_obj and peer_obj.height == update['height']:
            update['state'] = PeerMonitor.State.STUCK
        else:
            _cumulative_difficulty = get_block_cumulative_difficulty(update['height'])
            if update['cumulative_difficulty'] == _cumulative_difficulty:
                update['state'] = PeerMonitor.State.SYNC
            else:
                update['state'] = PeerMonitor.State.FORKED

    del update['_data']


@lock_decorator(key='peer_monitor', expire=60, auto_renewal=True)
@transaction.atomic
def peer_cmd():
    logger.info('Start')

    addresses = get_nodes_list()

    # set all peers unreachable, if will no update - peer will be unreachable
    PeerMonitor.objects.update(state=PeerMonitor.State.UNREACHABLE)

    # explore every peer and collect updates
    updates = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda address: explore_node(address, updates), addresses)

    # calculate state and apply updates
    for update in updates.values():
        if not update:
            continue

        logger.debug('Update: %r', update)

        peer_obj = PeerMonitor.objects.filter(ip=update['ip']).first()
        if not peer_obj:
            logger.info('Found new peer: %s', update['announced_address'])

        set_state(update, peer_obj)

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
