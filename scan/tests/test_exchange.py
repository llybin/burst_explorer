from unittest.case import TestCase

from django.core.cache import cache
from django.test import override_settings
from vcr import VCR

from scan.helpers.exchange import (
    EXCHANGE_CACHE_KEY,
    ExchangeData,
    get_cached_exchange_data,
    get_exchange_data,
    set_cache_exchange_data,
)

my_vcr = VCR(
    cassette_library_dir="scan/tests/fixtures/vcr/information",
    record_mode="once",
    decode_compressed_response=True,
)


class ExchangeAPITest(TestCase):
    @my_vcr.use_cassette("coingecko_success.yaml")
    def test_get_exchange_data(self):
        data = get_exchange_data()
        self.assertEqual(
            data,
            ExchangeData(
                price_usd=0.00533808,
                price_btc=6.847e-07,
                market_cap_usd=11131908.013570584,
                percent_change_24h=-4.392684830224021,
            ),
        )


class GetExchangeDataTest(TestCase):
    def setUp(self) -> None:
        cache.delete(EXCHANGE_CACHE_KEY)

    def test_no_data(self):
        self.assertEqual(get_cached_exchange_data(), ExchangeData())

    @override_settings(TEST_NET=True)
    def test_test_net(self):
        self.assertEqual(get_cached_exchange_data(), ExchangeData())

    @my_vcr.use_cassette("coingecko_success.yaml")
    def test_get_saved(self):
        data = get_exchange_data()
        set_cache_exchange_data(data)
        self.assertEqual(get_cached_exchange_data(), data)
