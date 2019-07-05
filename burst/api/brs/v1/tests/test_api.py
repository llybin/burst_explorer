from unittest import TestCase

import vcr

from burst.api.exceptions import ClientException, APIException
from burst.api.brs.v1.queries import QueryBase
from burst.api.brs import BrsApi

my_vcr = vcr.VCR(
    cassette_library_dir='burst/api/brs/v1/tests/fixtures/vcr',
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
        with self.assertRaises(APIException) as em:
            BrsApi('https://wallet.burst.devtrue.net').get_peer('178.48.21.1451')

        self.assertEqual(
            str(em.exception),
            "{'errorCode': 5, 'errorDescription': 'Unknown peer', 'requestProcessingTime': 2}"
        )


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


class GetUnconfirmedTransactionsTest(TestCase):
    @my_vcr.use_cassette('get_unconfirmed_transactions_multiout')
    def test_multiout(self):
        self.assertListEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_unconfirmed_transactions(),
            [
                {
                    "type": 0,
                    "subtype": 1,
                    "timestamp": 152020345,
                    "deadline": 1440,
                    "senderPublicKey": "95244648e02bb02fcc9d93b9e2d9ff5aac4f4eddaddf0b07bce5d2e287295455",
                    "amountNQT": "71856680037",
                    "feeNQT": "150000000",
                    "signature": "cf13b161509f78b60395a71e07b9a83bd2f495b4e612a2467c64f0b768519b0c45b9c4797010fae5b37fa072fc6f07975035a335e575d02f05f7af93e41250b0",  # NOQA
                    "signatureHash": "006be3c30835836d2df705a02d99bcdf7e637c0f1404c079de172b896e8e76aa",
                    "fullHash": "b6f50cd575ce35fc4df7e332bdd57e9cff30d92a248bc0b214914e670dbcd153",
                    "transaction": "18173658876804396470",
                    "attachment": {
                        "version.MultiOutCreation": 1,
                        "recipients": [
                            ["5775640609968742793", "10056387470"],
                            ["8134605299845103408", "10646786554"],
                            ["13963886526464512666", "10174613985"],
                            ["15292335569475861611", "10050574440"],
                            ["15421345662421390096", "10012112866"],
                            ["18248060628606727216", "10123985380"],
                            ["3581830426445587205", "10792219342"]
                        ]
                    },
                    "sender": "3606956930919944878",
                    "senderRS": "BURST-VNPG-8ZFT-5DC8-5WM56",
                    "height": 628533,
                    "version": 1,
                    "ecBlockId": "5188876724881306039",
                    "ecBlockHeight": 628522
                }
            ])

    @my_vcr.use_cassette('get_unconfirmed_transactions_single')
    def test_single(self):
        self.assertListEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_unconfirmed_transactions(),
            [
                {
                    "type": 0,
                    "subtype": 0,
                    "timestamp": 152024579,
                    "deadline": 1440,
                    "senderPublicKey": "18f6f49edb73a5528ee0b12a0f907db1a3baf98f9a4b9bf9e62710a79cc04e2d",
                    "recipient": "4476985392447067460",
                    "recipientRS": "BURST-R7C6-HU8Q-F9DR-5LDAW",
                    "amountNQT": "38540648977",
                    "feeNQT": "100000000",
                    "signature": "bc91e2534080efe239ef9696f8d4cab6229ef15a7d8e141c46d2ebbfa9e6110e890e200a37f5f30c3c58564bdb2be8f0ac3c29de11acdf8dfa6a114ea492a05c",  # NOQA
                    "signatureHash": "218d9b7057d14e0c63a73a40945592c489f07c061ff54af04fbac4dcdc1c238d",
                    "fullHash": "d233bcd327759b34c6e5d696928e02bd0b567383f282b2c434d9a7b47acc708d",
                    "transaction": "3790752325278905298",
                    "sender": "6887101586189604106",
                    "senderRS": "BURST-SPAC-EWWF-CRX2-78Z6Z",
                    "height": 628552,
                    "version": 1,
                    "ecBlockId": "8357613288046163076",
                    "ecBlockHeight": 628544
                }
            ])

    @my_vcr.use_cassette('get_unconfirmed_transactions_multiout_same')
    def test_multiout_same(self):
        self.assertListEqual(
            BrsApi('https://wallet.burst.devtrue.net').get_unconfirmed_transactions(),
            [
                {
                    "type": 0,
                    "subtype": 2,
                    "timestamp": 153138073,
                    "deadline": 1440,
                    "senderPublicKey": "603631d84654e2097310b721552c4a5ed9dc7eca5ea8cfd3b437f79546a32776",
                    "amountNQT": "400000000",
                    "feeNQT": "735000",
                    "signature": "0eb48eec5130c497fe46ee0c27bd075dad012d81541b4f4ec1aa8a8e42211d06197eb54747ea680a32ad042de622b6c0eea002372d64331c73e617ece320c052",  # NOQA
                    "signatureHash": "c95757e7ac3460e55f88d6bbf24b9922e9e2980ab67a8bb7d541e10d1e5a87d8",
                    "fullHash": "2c019032c782af1c4092da64325574fea496f1b0b4d7acdf3ee84d75c4057151",
                    "transaction": "2067014546044748076",
                    "attachment": {
                        "version.MultiSameOutCreation": 1,
                        "recipients": [
                            "820256820168033388",
                            "8087908814943479341"
                        ]},
                    "sender": "820256820168033388",
                    "senderRS": "BURST-C35E-9FMD-NUDP-25KSQ",
                    "height": 2147483647,
                    "version": 1,
                    "ecBlockId": "12109381587560828069",
                    "ecBlockHeight": 633157
                }
            ])
