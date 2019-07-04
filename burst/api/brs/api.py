""" BRS: https://github.com/burst-apps-team/burstcoin/
"""

import requests
from requests.exceptions import RequestException
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from burst.api.exceptions import APIException, ClientException
from burst.api.typing import JSONType
from burst.api.brs import queries


class BrsApi:
    """ The BrsApi class provides convenient access to Brs's API.
    """
    endpoint = 'burst'
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

        self.node_url = node_address
        self._session = requests.session()

    def _close_session(self) -> None:
        """ Close session if exists"""
        if self._session:
            self._session.close()

    def __del__(self) -> None:
        """ Destructor """
        self._close_session()

    def _request_get(self, query: queries.QueryBase) -> JSONType:
        """ Make HTTP request using requests module """
        url = '{}/{}'.format(self.node_url, self.endpoint)

        try:
            response = self._session.get(url, params=query.params, timeout=query.timeout)
            response.raise_for_status()
        except RequestException as e:
            raise APIException('network', e)

        try:
            json_response = response.json()
        except ValueError as e:
            raise APIException('malformed_json', e)

        query.validate_response(json_response)

        return json_response

    def get_peers(self) -> list:
        return self._request_get(queries.GetPeers())['peers']

    def get_peer(self, peer_ip_address: str) -> dict:
        return self._request_get(queries.GetPeer({'peer': peer_ip_address}))

    def get_block_chain_status(self) -> dict:
        return self._request_get(queries.GetBlockChainStatus())

    def get_mining_info(self) -> dict:
        return self._request_get(queries.GetMiningInfo())

    def get_state(self) -> dict:
        return self._request_get(queries.GetState())

    def get_unconfirmed_transactions(self) -> list:
        return self._request_get(queries.GetUnconfirmedTransactions())['unconfirmedTransactions']
