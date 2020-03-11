from django.conf import settings

from scan.helpers.exchange import get_cached_exchange_data


def settings_context_processor(request):
    return {
        "google_tracking_id": settings.GOOGLE_TRACKING_ID,
        "test_net": settings.TEST_NET,
        "wallet_url": settings.WALLET_URL,
        "burst_info": {"exchange": get_cached_exchange_data()},
    }
