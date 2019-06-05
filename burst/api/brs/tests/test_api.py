from unittest import TestCase

import vcr

from burst.api.exceptions import ClientException, APIException
from burst.api.brs.queries import QueryBase
from burst.api.brs import BrsApi

my_vcr = vcr.VCR(
    cassette_library_dir='burst/api/brs/tests/fixtures/vcr',
    record_mode='once',
    decode_compressed_response=True,
)


class TestQuery(QueryBase):
    _request_type = 'Test'


class BrsApiTest(TestCase):
    def test_node_url_ok(self):
        self.assertEqual(
            BrsApi('http://127.0.0.1:80').node_url,
            'http://127.0.0.1:80'
        )

        self.assertEqual(
            BrsApi('127.0.0.1:80').node_url,
            'http://127.0.0.1:80'
        )

    def test_node_url_fail(self):
        with self.assertRaises(ClientException) as em:
            BrsApi('')

        self.assertEqual(
            str(em.exception),
            "Not valid address"
        )

        with self.assertRaises(ClientException) as em:
            BrsApi('127.0')

        self.assertEqual(
            str(em.exception),
            "Not valid address"
        )

    def test_request_get_fail_network(self):
        with self.assertRaises(APIException):
            BrsApi('http://127.0.0.2:1234')._request_get(TestQuery())

    @my_vcr.use_cassette('test_query_malformed_json')
    def test_request_get_malformed_json(self):
        with self.assertRaises(APIException):
            BrsApi('https://wallet.burst.devtrue.net')._request_get(TestQuery())

    @my_vcr.use_cassette('test_query_malformed_data')
    def test_request_get_malformed_data(self):
        class Temp(TestQuery):
            _json_schema = {
                "type": "array",
                "items": {"type": "string"}
            }

        with self.assertRaises(APIException):
            BrsApi('https://wallet.burst.devtrue.net')._request_get(Temp())


class GetPeersTest(TestCase):
    @my_vcr.use_cassette('get_peers')
    def test_ok(self):
        self.assertListEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_peers(),
            ["68.65.35.34", "[2a01:4f8:bc:aa1:0:0:0:b67c]"])


class GetPeerTest(TestCase):
    @my_vcr.use_cassette('get_peer_offline')
    def test_offline(self):
        self.assertDictEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_peer('68.65.35.34'),
            {
                "state": 0,
                "announcedAddress": "68.65.35.34",
                "shareAddress": True,
                "downloadedVolume": 0,
                "uploadedVolume": 0,
                "application": None,
                "version": "v0.0.0",
                "platform": None,
                "blacklisted": False,
                "lastUpdated": 0,
                "requestProcessingTime": 0
            })

    @my_vcr.use_cassette('get_peer_online')
    def test_online(self):
        self.assertDictEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_peer('178.48.21.145'),
            {
                "state": 0,
                "announcedAddress": "178.48.21.145",
                "shareAddress": True,
                "downloadedVolume": 134948,
                "uploadedVolume": 117110,
                "application": "BRS",
                "version": "v2.3.0",
                "platform": "Q-H2",
                "blacklisted": False,
                "lastUpdated": 151846101,
                "requestProcessingTime": 0
            })

    @my_vcr.use_cassette('get_peer_error')
    def test_error(self):
        self.assertDictEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_peer('178.48.21.1451'),
            {
                "errorCode": 5,
                "errorDescription": "Unknown peer",
                "requestProcessingTime": 2
            })


class GetBlockChainStatusTest(TestCase):
    @my_vcr.use_cassette('get_block_chain_status')
    def test_ok(self):
        self.assertDictEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_block_chain_status(),
            {
                "application": "BRS",
                "version": "v2.3.0",
                "time": 151999882,
                "lastBlock": "3461701356085316422",
                "cumulativeDifficulty": "60714757902044174379",
                "numberOfBlocks": 628451,
                "lastBlockchainFeeder": "75.100.126.227",
                "lastBlockchainFeederHeight": 628450,
                "isScanning": False,
                "requestProcessingTime": 0
            })


class GetMiningInfoTest(TestCase):
    @my_vcr.use_cassette('get_mining_info')
    def test_ok(self):
        self.assertDictEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_mining_info(),
            {
                "height": "628451",
                "generationSignature": "f25a6d8b694382fddfef15057e969cd3db6dee8c982f392a7ca4785f0507f9cb",
                "baseTarget": "68942",
                "requestProcessingTime": 0
            })


class GetStateTest(TestCase):
    @my_vcr.use_cassette('get_state')
    def test_ok(self):
        self.assertDictEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_state(),
            {
                "application": "BRS",
                "version": "v2.3.0",
                "time": 152000464,
                "lastBlock": "3461701356085316422",
                "cumulativeDifficulty": "60714757902044174379",
                "totalEffectiveBalanceNXT": 2094200481,
                "numberOfBlocks": 628451,
                "numberOfTransactions": 8075239,
                "numberOfAccounts": 707241,
                "numberOfAssets": 400,
                "numberOfOrders": 2994,
                "numberOfAskOrders": 2657,
                "numberOfBidOrders": 337,
                "numberOfTrades": 111241,
                "numberOfTransfers": 119844,
                "numberOfAliases": 57700,
                "numberOfPeers": 611,
                "numberOfUnlockedAccounts": 0,
                "lastBlockchainFeeder": "84.10.50.53",
                "lastBlockchainFeederHeight": 628450,
                "isScanning": False,
                "availableProcessors": 2,
                "maxMemory": 524288000,
                "totalMemory": 188743680,
                "freeMemory": 78025328,
                "requestProcessingTime": 9608
            })
