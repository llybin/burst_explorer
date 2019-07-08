""" https://github.com/burst-apps-team/burstcoin/blob/master/t/lib/BURST/API/RequestTypes.pm
"""

import abc

from jsonschema import validate, ValidationError

from burst.api.exceptions import ClientException, APIException


class QueryBase(abc.ABC):
    _request_type_field = 'requestType'
    _error_field = 'errorCode'
    _response_json_schema = None
    _params = {}
    _required_params = set()
    _optional_params = set()
    timeout = 3

    @property
    @abc.abstractmethod
    def _request_type(self):
        pass

    @property
    @abc.abstractmethod
    def _http_method(self):
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
    def http_method(self) -> str:
        return self._http_method

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
        # TODO: return true or raise
        if not self._response_json_schema:
            return True

        if self._error_field in data:
            raise APIException(data)

        try:
            validate(data, self._response_json_schema)
        except ValidationError as e:
            raise APIException('malformed_data', e)
        else:
            return True


class GetPeers(QueryBase):
    _request_type = 'getPeers'
    _http_method = 'GET'
    _response_json_schema = {
        "type": "object",
        "properties": {
            "peers": {"type": "array"},
            "requestProcessingTime": {"type": "number"},
        },
        "required": [
            "peers",
            "requestProcessingTime"
        ]
    }


class GetPeer(QueryBase):
    _request_type = 'getPeer'
    _http_method = 'GET'
    _required_params = {'peer'}
    _response_json_schema = {
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
        "required": [
            "state",
            "announcedAddress",
            "shareAddress",
            "downloadedVolume",
            "uploadedVolume",
            "application",
            "version",
            "platform",
            "blacklisted",
            "lastUpdated",
            "requestProcessingTime"
        ]
    }


class GetBlockChainStatus(QueryBase):
    _request_type = 'getBlockchainStatus'
    _http_method = 'GET'
    _response_json_schema = {
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
        "required": [
            "application",
            "version",
            "time",
            "lastBlock",
            "cumulativeDifficulty",
            "numberOfBlocks",
            "lastBlockchainFeeder",
            "lastBlockchainFeederHeight",
            "isScanning",
            "requestProcessingTime"
        ]
    }


class GetMiningInfo(QueryBase):
    _request_type = 'getMiningInfo'
    _http_method = 'GET'
    _response_json_schema = {
        "type": "object",
        "properties": {
            "height": {"type": "string"},
            "generationSignature": {"type": "string"},
            "baseTarget": {"type": "string"},
            "requestProcessingTime": {"type": "number"},
        },
        "required": [
            "height",
            "generationSignature",
            "baseTarget",
            "requestProcessingTime"
        ]
    }


class GetState(QueryBase):
    _request_type = 'getState'
    _http_method = 'GET'
    _response_json_schema = {
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
        "required": [
            "application",
            "version",
            "time",
            "lastBlock",
            "cumulativeDifficulty",
            "totalEffectiveBalanceNXT",
            "numberOfBlocks",
            "numberOfTransactions",
            "numberOfAccounts",
            "numberOfAssets",
            "numberOfOrders",
            "numberOfAskOrders",
            "numberOfBidOrders",
            "numberOfTrades",
            "numberOfTransfers",
            "numberOfAliases",
            "numberOfPeers",
            "numberOfUnlockedAccounts",
            "lastBlockchainFeeder",
            "lastBlockchainFeederHeight",
            "isScanning",
            "availableProcessors",
            "maxMemory",
            "totalMemory",
            "freeMemory",
            "requestProcessingTime",
        ]
    }
    timeout = 10


class GetUnconfirmedTransactions(QueryBase):
    _request_type = 'getUnconfirmedTransactions'
    _http_method = 'GET'
    _response_json_schema = {
        "type": "object",
        "properties": {
            "unconfirmedTransactions": {"type": "array"},
            "requestProcessingTime": {"type": "number"},
        },
        "required": [
            "unconfirmedTransactions",
            "requestProcessingTime"
        ]
    }
    # TODO: validate each
    # {"type":0,"subtype":0,"timestamp":154715780,"deadline":1000,"senderPublicKey":"447db598ab0b8b128516b3a70b9d87ea4cdb460fb4c550167cbfceda865fb03d","recipient":"13493329130306648054","amountNQT":10000000,"feeNQT":735000,"ecBlockHeight":639673,"ecBlockId":"3483458127310479448","signature":"9de1f780425b7bc95d63982196ab3349dcfb4fb1297a1ab88db411693eb14b02d1046a048aba0210294448d21d9978ce9b69b4bf27faefbba4c93c49a2ff3a4a","attachment":{},"version":1}
