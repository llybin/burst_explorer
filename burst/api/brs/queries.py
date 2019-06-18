""" https://github.com/burst-apps-team/burstcoin/blob/master/t/lib/BURST/API/RequestTypes.pm
"""

import abc

from jsonschema import validate, ValidationError

from burst.api.exceptions import ClientException, APIException


class QueryBase(abc.ABC):
    _request_type_field = 'requestType'
    _json_schema = None
    _params = {}
    _required_params = set()
    _optional_params = set()
    timeout = 1

    @property
    @abc.abstractmethod
    def _request_type(self):
        pass

    def __init__(self, params: dict = None) -> None:
        self.validate_params(params)
        if params:
            self._params = params

    def __str__(self) -> str:
        return self._request_type

    @property
    def request_type(self) -> str:
        return self._request_type

    @property
    def params(self) -> dict:
        return {
            self._request_type_field: self._request_type,
            **self._params}

    def validate_params(self, params: dict or None) -> None:
        if not (params or self._required_params or self._optional_params):
            return

        if params:
            params_keys = set(params.keys())
        else:
            params_keys = set()

        if self._required_params:
            omitted_params = self._required_params - params_keys
            if omitted_params:
                raise ClientException('Omitted required params: {}'.format(omitted_params))

        unknown_params = params_keys - (self._required_params | self._optional_params)
        if unknown_params:
            raise ClientException('Unknown params: {}'.format(unknown_params))

    def validate_response(self, data) -> bool:
        if not self._json_schema:
            return True

        try:
            validate(data, self._json_schema)
        except ValidationError as e:
            raise APIException('malformed_data', e)
        else:
            return True


class GetPeers(QueryBase):
    _request_type = 'getPeers'
    _json_schema = {
        "type": "object",
        "properties": {
            "peers": {"type": "array"},
            "requestProcessingTime": {"type": "number"},
        },
        "required": ["peers"]
    }


class GetPeer(QueryBase):
    _request_type = 'getPeer'
    _required_params = {'peer'}
    _json_schema = {
        "type": "object",
        "properties": {
            "state": {"type": "number"},
            "announcedAddress": {"type": ["string", "null"]},
            "shareAddress": {"type": "boolean"},
            "downloadedVolume": {"type": "number"},
            "uploadedVolume": {"type": "number"},
            "application": {"type": ["string", "null"]},
            "version": {"type": "string"},
            "platform": {"type": ["string", "null"]},
            "blacklisted": {"type": "boolean"},
            "lastUpdated": {"type": "number"},
            "requestProcessingTime": {"type": "number"},
        },
    }


class GetBlockChainStatus(QueryBase):
    _request_type = 'getBlockchainStatus'
    _json_schema = {
        "type": "object",
        "properties": {
            "application": {"type": "string"},
            "version": {"type": "string"},
            "time": {"type": "number"},
            "lastBlock": {"type": "string"},
            "cumulativeDifficulty": {"type": "string"},
            "numberOfBlocks": {"type": "number"},
            "lastBlockchainFeeder": {"type": "string"},
            "lastBlockchainFeederHeight": {"type": "number"},
            "isScanning": {"type": "boolean"},
            "requestProcessingTime": {"type": "number"},
        },
    }


class GetMiningInfo(QueryBase):
    _request_type = 'getMiningInfo'
    _json_schema = {
        "type": "object",
        "properties": {
            "height": {"type": "string"},
            "generationSignature": {"type": "string"},
            "baseTarget": {"type": "string"},
            "requestProcessingTime": {"type": "number"},
        },
    }


class GetState(QueryBase):
    _request_type = 'getState'
    _json_schema = {
        "type": "object",
        "properties": {
            "application": {"type": "string"},
            "version": {"type": "string"},
            "time": {"type": "number"},
            "lastBlock": {"type": "string"},
            "cumulativeDifficulty": {"type": "string"},
            "totalEffectiveBalanceNXT": {"type": "number"},
            "numberOfBlocks": {"type": "number"},
            "numberOfTransactions": {"type": "number"},
            "numberOfAccounts": {"type": "number"},
            "numberOfAssets": {"type": "number"},
            "numberOfOrders": {"type": "number"},
            "numberOfAskOrders": {"type": "number"},
            "numberOfBidOrders": {"type": "number"},
            "numberOfTrades": {"type": "number"},
            "numberOfTransfers": {"type": "number"},
            "numberOfAliases": {"type": "number"},
            "numberOfPeers": {"type": "number"},
            "numberOfUnlockedAccounts": {"type": "number"},
            "lastBlockchainFeeder": {"type": "string"},
            "lastBlockchainFeederHeight": {"type": "number"},
            "isScanning": {"type": "boolean"},
            "availableProcessors": {"type": "number"},
            "maxMemory": {"type": "number"},
            "totalMemory": {"type": "number"},
            "freeMemory": {"type": "number"},
            "requestProcessingTime": {"type": "number"},
        },
    }
    timeout = 10


class GetUnconfirmedTransactions(QueryBase):
    _request_type = 'getUnconfirmedTransactions'
