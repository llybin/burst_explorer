""" https://github.com/burst-apps-team/burstcoin/blob/master/t/lib/BURST/API/RequestTypes.pm
"""

import abc

from burst.api.brs.v1.queries import QueryBase as QueryBaseApiV1


class QueryBase(QueryBaseApiV1, abc.ABC):
    _http_method = "POST"
    _error_field = "error"
    _protocol_field = "protocol"
    _protocol = "B1"

    @property
    def params(self) -> dict:
        return {
            self._request_type_field: self._request_type,
            self._protocol_field: self._protocol,
            **self._params,
        }


class GetPeers(QueryBase):
    _request_type = "getPeers"
    _response_json_schema = {
        "type": "object",
        "properties": {"peers": {"type": "array"}},
        "required": ["peers"],
    }


class GetInfo(QueryBase):
    _request_type = "getInfo"
    _response_json_schema = {
        "type": "object",
        "properties": {
            "announcedAddress": {"type": "string"},
            "application": {"type": "string"},
            "version": {"type": "string"},
            "platform": {"type": "string"},
            "shareAddress": {"type": "boolean"},
        },
        "required": [
            "announcedAddress",
            "application",
            "version",
            "platform",
            "shareAddress",
        ],
    }


class GetCumulativeDifficulty(QueryBase):
    _request_type = "getCumulativeDifficulty"
    _response_json_schema = {
        "type": "object",
        "properties": {
            "cumulativeDifficulty": {"type": "string"},
            "blockchainHeight": {"type": "integer"},
        },
        "required": ["cumulativeDifficulty", "blockchainHeight"],
    }


class AddPeers(QueryBase):
    _request_type = "addPeers"


class GetMilestoneBlockIds(QueryBase):
    _request_type = "getMilestoneBlockIds"


class GetNextBlockIds(QueryBase):
    _request_type = "getNextBlockIds"


class GetBlocksFromHeight(QueryBase):
    _request_type = "getBlocksFromHeight"


class GetNextBlocks(QueryBase):
    _request_type = "getNextBlocks"


class GetUnconfirmedTransactions(QueryBase):
    _request_type = "getUnconfirmedTransactions"


class ProcessBlock(QueryBase):
    _request_type = "processBlock"


class ProcessTransactions(QueryBase):
    _request_type = "processTransactions"


class GetAccountBalance(QueryBase):
    _request_type = "getAccountBalance"


class GetAccountRecentTransactions(QueryBase):
    _request_type = "getAccountRecentTransactions"


# TODO: tests
