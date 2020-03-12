from dataclasses import dataclass

from django.conf import settings
from django.core.cache import cache
from pycoingecko import CoinGeckoAPI

EXCHANGE_CACHE_KEY = "exchange_data"


@dataclass
class ExchangeData:
    price_usd: float = 0
    price_btc: float = 0
    market_cap_usd: float = 0
    percent_change_24h: float = 0


def get_cached_exchange_data() -> ExchangeData:
    if settings.TEST_NET:
        return ExchangeData()

    data = cache.get(EXCHANGE_CACHE_KEY)
    return ExchangeData(**data) if data else ExchangeData()


def set_cache_exchange_data(data: ExchangeData):
    cache.set(EXCHANGE_CACHE_KEY, data.__dict__, 3600)


def get_exchange_data() -> ExchangeData:
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
