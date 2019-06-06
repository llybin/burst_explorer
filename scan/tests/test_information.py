from unittest import TestCase

import vcr

from scan.information import get_exchange_info


my_vcr = vcr.VCR(
    cassette_library_dir='scan/tests/fixtures/vcr/information',
    record_mode='once',
    decode_compressed_response=True,
)


class GetExchangeInfoTest(TestCase):
    @my_vcr.use_cassette('success')
    def test_ok(self):
        self.skipTest("TODO: refact and mock")
        self.assertDictEqual(
            get_exchange_info(),
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
