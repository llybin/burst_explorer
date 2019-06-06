import requests
from django.core.cache import cache
from requests.exceptions import RequestException
from sentry_sdk import capture_exception

from burst.api.typing import JSONType


def get_exchange_info() -> JSONType:
    # TODO: move caching, refact
    key = "coinmarketcap"

    data = cache.get(key)

    if not data:
        try:
            response = requests.get('https://api.coinmarketcap.com/v1/ticker/burst/')
            response.raise_for_status()
            data = response.json()[0]
            data['price_usd'] = float(data['price_usd'])
            data['24h_volume_usd'] = float(data['24h_volume_usd'])
            data['market_cap_usd'] = float(data['market_cap_usd'])
            data['percent_change_24h'] = float(data['percent_change_24h'])
        except (RequestException, ValueError, IndexError) as e:
            capture_exception(e)
            return {}

    cache.set(key, data, 300)

    return data
