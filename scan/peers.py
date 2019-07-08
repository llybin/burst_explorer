import concurrent.futures
import logging
import random
import socket
from functools import lru_cache
from urllib.parse import urlparse

import requests
from cache_memoize import cache_memoize
from django import forms
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from requests.exceptions import RequestException

from burst.api.brs.p2p import P2PApi
from burst.api.exceptions import BurstException
from scan.decorators import lock_decorator
from scan.models import PeerMonitor
from scan.helpers import get_last_height


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

    updates[ip] = dict(
        ip=ip,
        country_code=get_country_by_ip(ip),
        announced_address=peer_info['announcedAddress'],
        application=peer_info['application'],
        platform=peer_info['platform'],
        version=peer_info['version'],
        height=peer_info['blockchainHeight'],
        cumulative_difficulty=peer_info['cumulativeDifficulty'],
    )


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
    for peer in settings.BRS_BOOTSTRAP_PEERS:
        if peer not in addresses_other:
            addresses_other.append(peer)

    # mix it
    random.shuffle(addresses_offline)
    random.shuffle(addresses_other)

    # first UNREACHABLE
    return addresses_offline + addresses_other


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

    last_height = get_last_height()
    logger.info('Last height: %d', last_height)

    # calculate state and apply updates
    for update in updates.values():
        if not update:
            continue

        logger.debug('Update: %r', update)

        peer_obj = PeerMonitor.objects.filter(ip=update['ip']).first()
        if not peer_obj:
            logger.info('Found new peer: %s', update['announced_address'])

        # state
        if update['height'] == last_height:
            # TODO: if eq cumulative_difficulty - online else forked
            update['state'] = PeerMonitor.State.ONLINE
        elif update['height'] > last_height:
            update['state'] = PeerMonitor.State.FORKED
        else:
            if peer_obj and peer_obj.height == update['height']:
                update['state'] = PeerMonitor.State.STUCK
            else:
                # TODO: if eq cumulative_difficulty of height - sync else forked
                update['state'] = PeerMonitor.State.SYNC

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
    # TODO: delete lifetime - downtime > 30*24*12
    # TODO: last available time?
    PeerMonitor.objects.update(
        availability=100 - (F('downtime') / F('lifetime') * 100),
        modified_at=timezone.now()
    )
    logger.info('Done')
