import logging

import requests
from cache_memoize import cache_memoize
from django.conf import settings
from django.db import transaction
from django.db.models import F
from django import forms
from requests.exceptions import RequestException

from burst.api.brs import BrsApi
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
        return json_response['geoplugin_countryCode'] or ''
    except (RequestException, ValueError, KeyError):
        return ''


def normalize_version(version: str) -> str or None:
    return None if version in ['v0.0.0', ''] else version


class PeerMonitorForm(forms.ModelForm):
    class Meta:
        model = PeerMonitor
        fields = '__all__'


def node_with_port(node: str) -> str:
    ports = {8125, 8124, 2083, 80, 443, 8080, 8000, 5000, 6876}

    if ':' not in node:
        for x in ports:
            _node = 'http{}://{}:{}'.format('http' if x != 443 else 'https', node, x)
            try:
                BrsApi(_node).get_peers()
                logger.info('Port found: %d', x)
                node = _node
                break
            except BurstException:
                continue

    elif ':443' in node and 'https' not in node:
        node = 'https://{}'.format(node)

    return node


def explore_node(node: str):
    logger.info('Node: %s', node)

    try:
        node_api = BrsApi(node_with_port(node))
        peers = node_api.get_peers()
        for peer in peers:
            peer_detail = node_api.get_peer(peer)
            peer = peer.replace('[', '').replace(']', '')  # ipv6
            logger.info('Peer: %s, state: %d', peer, peer_detail['state'])
            # NON_CONNECTED, CONNECTED, DISCONNECTED
            if peer_detail['state'] == 1:
                peer_obj = PeerMonitor.objects.filter(address=peer).first()
                if not peer_obj:
                    logger.info('Found new peer: %s', peer)

                form = PeerMonitorForm(dict(
                    address=peer,
                    country_code=get_country_by_ip(peer),
                    announced_address=peer_detail['announcedAddress'],
                    application=peer_detail['application'],
                    version=normalize_version(peer_detail['version']),
                    proofs_online=peer_obj.proofs_online + 1 if peer_obj else 1
                ), instance=peer_obj)

                if form.is_valid():
                    form.save()
                else:
                    logger.warning('Not valid data: %r', form.errors)

    except BurstException:
        logger.warning("Can't connect to node: %s", node)


@lock_decorator(key='peer_monitor', expire=300, auto_renewal=True)
@transaction.atomic
def peer_cmd():
    logger.info('Start')

    PeerMonitor.objects.update(proofs_online=0)

    for node in settings.BRS_BOOTSTRAP_PEERS:
        explore_node(node)

    for node in PeerMonitor.objects.values_list('announced_address', flat=True):
        explore_node(node)

    PeerMonitor.objects.update(lifetime=F('lifetime') + 1)
    PeerMonitor.objects.filter(
        proofs_online=0
    ).update(downtime=F('downtime') + 1)

    # 100 - (downtime / lifetime) * 100

    logger.info('Done')
