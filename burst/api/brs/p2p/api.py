""" https://github.com/burst-apps-team/burstcoin/tree/develop/src/brs/peer
"""

from django.conf import settings

from burst.api.brs.p2p import queries
from burst.api.brs.v1.api import BrsApiBase


class P2PApi(BrsApiBase):
    """ The P2PApi class provides convenient access to P2P API.
    """

    headers = {"User-Agent": f"BRS/{settings.BRS_P2P_VERSION}"}

    _default_port = settings.DEFAULT_P2P_PORT

    def get_peers(self) -> list:
        return self._request(queries.GetPeers())["peers"]

    def get_info(self) -> dict:
        return self._request(queries.GetInfo())

    def get_cumulative_difficulty(self) -> dict:
        return self._request(queries.GetCumulativeDifficulty())


# TODO: tests
