from unittest.case import TestCase

import pytest
from django.test import override_settings

from scan.caching_data.exchange import CachingExchangeData, ExchangeData


class ExchangeAPITest(TestCase):
    @pytest.mark.vcr("coingecko_success.yaml")
    def test_get_exchange_data(self):
        data = CachingExchangeData().live_data
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
        CachingExchangeData().clear_cached_data()

    @pytest.mark.vcr("coingecko_success.yaml")
    def test_live_if_empty(self):
        self.assertEqual(
            CachingExchangeData().cached_data,
            ExchangeData(
                price_usd=0.00533808,
                price_btc=6.847e-07,
                market_cap_usd=11131908.013570584,
                percent_change_24h=-4.392684830224021,
            ),
        )

    @override_settings(TEST_NET=True)
    def test_test_net(self):
        self.assertEqual(CachingExchangeData().cached_data, ExchangeData())

    @pytest.mark.vcr("coingecko_success.yaml")
    def test_get_saved(self):
        data = CachingExchangeData()._get_live_data()
        CachingExchangeData().update_data(data)
        self.assertEqual(CachingExchangeData().cached_data, data)
