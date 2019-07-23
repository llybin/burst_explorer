from unittest import TestCase

import vcr
from django.test import override_settings

from scan.helpers import get_exchange_info, get_pending_txs

my_vcr = vcr.VCR(
    cassette_library_dir='scan/tests/fixtures/vcr/information',
    record_mode='once',
    decode_compressed_response=True,
)


class GetPendingTxs(TestCase):
    @my_vcr.use_cassette('get_pending_txs')
    def test_ok(self):
        txs = get_pending_txs()
        self.assertEqual(len(txs), 15)
        self.assertEqual(txs[14]['multiout'], 2)
        self.assertEqual(txs[0]['multiout'], 6)


class GetExchangeInfoTest(TestCase):
    @my_vcr.use_cassette('coinmarketcap_success')
    def test_ok(self):
        self.assertDictEqual(
            get_exchange_info(_refresh=True),
            {
                "id": "burst",
                "name": "Burst",
                "symbol": "BURST",
                "rank": "437",
                "price_usd": 0.002973448,
                "price_btc": "0.00000038",
                "24h_volume_usd": 38229.8232334,
                "market_cap_usd": 6078590.0,
                "available_supply": "2044290023.0",
                "total_supply": "2044290023.0",
                "max_supply": "2158812800.0",
                "percent_change_1h": "-3.81",
                "percent_change_24h": -5.14,
                "percent_change_7d": "-4.53",
                "last_updated": "1559812981"
            }
        )

    @my_vcr.use_cassette('coinmarketcap_many_requests')
    def test_many_requests_error(self):
        self.assertDictEqual(
            get_exchange_info(_refresh=True),
            {
                'price_usd': 0,
                '24h_volume_usd': 0,
                'market_cap_usd': 0,
                'percent_change_24h': 0,
            }
        )

    @override_settings(TEST_NET=True)
    def test_test_net(self):
        self.assertDictEqual(
            get_exchange_info(_refresh=True),
            {
                'price_usd': 0,
                '24h_volume_usd': 0,
                'market_cap_usd': 0,
                'percent_change_24h': 0,
            }
        )
