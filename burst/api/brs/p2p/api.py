""" https://github.com/burst-apps-team/burstcoin/tree/develop/src/brs/peer
"""

from burst.api.brs.v1.api import BrsApiBase
from burst.api.brs.p2p import queries


class P2PApi(BrsApiBase):
    """ The P2PApi class provides convenient access to P2P API.
    """
    headers = {'User-Agent': 'BRS/2.4.0'}
    _default_port = 8123  # TODO: settings testnet

    def get_peers(self) -> list:
        return self._request(queries.GetPeers())['peers']

    def get_info(self) -> dict:
        return self._request(queries.GetInfo())

    def get_cumulative_difficulty(self) -> dict:
        return self._request(queries.GetCumulativeDifficulty())

# TODO: tests
