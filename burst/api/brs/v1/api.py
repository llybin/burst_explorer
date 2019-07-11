""" https://github.com/burst-apps-team/burstcoin/tree/develop/src/brs/http
"""

from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from burst.api.exceptions import APIException, ClientException
from burst.api.typing import JSONType
from burst.api.brs.v1 import queries


class BrsApiBase:
    endpoint = 'burst'
    headers = None
    _default_port = settings.DEFAULT_API_PORT
    _session = None

    def __init__(self, node_address: str) -> None:
        """ Constructor
        :param node_address: domain or ip address
        """
        if not node_address.startswith('http'):
            node_address = 'http://{}'.format(node_address)

        validate = URLValidator()
        try:
            validate(node_address)
        except ValidationError:
            raise ClientException('Not valid address')

        parsed_url = urlparse(node_address)

        if not parsed_url.port and not parsed_url.query:
            node_address = '{}:{}'.format(node_address, self._default_port)

        self.node_url = node_address
        self._session = requests.session()

    def _close_session(self) -> None:
        """ Close session if exists"""
        if self._session:
            self._session.close()

    def __del__(self) -> None:
        """ Destructor """
        self._close_session()

    def _request(self, query: queries.QueryBase) -> JSONType:
        """ Make HTTP request using requests module """
        url = '{}/{}'.format(self.node_url, self.endpoint)

        try:
            response = self._session.request(
                query.http_method,
                url,
                headers=self.headers,
                json=query.params if query.http_method == 'POST' else None,
                params=query.params if query.http_method == 'GET' else None,
                timeout=query.timeout,
                verify=False
            )
            response.raise_for_status()
        except RequestException as e:
            raise APIException('network', e)

        try:
            json_response = response.json()
        except ValueError as e:
            raise APIException('malformed_json', e)

        query.validate_response(json_response)

        return json_response


class BrsApi(BrsApiBase):
    """ The BrsApi class provides convenient access to Brs API.
    """

    def get_peers(self) -> list:
        return self._request(queries.GetPeers())['peers']

    def get_peer(self, peer_ip_address: str) -> dict:
        return self._request(queries.GetPeer({'peer': peer_ip_address}))

    def get_block_chain_status(self) -> dict:
        return self._request(queries.GetBlockChainStatus())

    def get_mining_info(self) -> dict:
        return self._request(queries.GetMiningInfo())

    def get_state(self) -> dict:
        return self._request(queries.GetState())

    def get_unconfirmed_transactions(self) -> list:
        return self._request(queries.GetUnconfirmedTransactions())['unconfirmedTransactions']
