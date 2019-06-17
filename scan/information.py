import requests
from django.conf import settings
from cache_memoize import cache_memoize
from requests.exceptions import RequestException
from sentry_sdk import capture_exception


@cache_memoize(600)
def get_exchange_info() -> dict:
    if settings.TEST_NET:
        return {
            'price_usd': 0,
            '24h_volume_usd': 0,
            'market_cap_usd': 0,
            'percent_change_24h': 0,
        }

    try:
        response = requests.get('https://api.coinmarketcap.com/v1/ticker/burst/')
        response.raise_for_status()
        data = response.json()[0]
        data['price_usd'] = float(data['price_usd'])
        data['24h_volume_usd'] = float(data['24h_volume_usd'])
        data['market_cap_usd'] = float(data['market_cap_usd'])
        data['percent_change_24h'] = float(data['percent_change_24h'])
        return data
    except (RequestException, ValueError, IndexError) as e:
        capture_exception(e)
        return {
            'price_usd': 0,
            '24h_volume_usd': 0,
            'market_cap_usd': 0,
            'percent_change_24h': 0,
        }
