from dataclasses import dataclass

from django.conf import settings
from pycoingecko import CoinGeckoAPI

from scan.caching_data.base import CachingDataBase


@dataclass
class ExchangeData:
    price_usd: float = 0
    price_btc: float = 0
    market_cap_usd: float = 0
    percent_change_24h: float = 0


class CachingExchangeData(CachingDataBase):
    _cache_key = "exchange_data"
    _cache_expiring = 3600
    live_if_empty = True
    default_data_if_empty = ExchangeData()

    @property
    def cached_data(self):
        if settings.TEST_NET:
            return self.default_data_if_empty
        return super().cached_data

    def _loads(self, data):
        return ExchangeData(**data)

    def _dumps(self, data):
        return data.__dict__

    def _get_live_data(self):
        if settings.TEST_NET:
            return self.default_data_if_empty

        cg = CoinGeckoAPI()
        response = cg.get_price(
            ids="burst",
            vs_currencies=["usd", "btc"],
            include_market_cap="true",
            include_24hr_change="true",
        )["burst"]

        return ExchangeData(
            price_usd=response["usd"],
            price_btc=response["btc"],
            market_cap_usd=response["usd_market_cap"],
            percent_change_24h=response["usd_24h_change"],
        )
