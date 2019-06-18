from django.conf import settings

from scan.helpers import get_exchange_info


def settings_context_processor(request):
    return {
        'account_name_force': settings.ACCOUNTS_NAME_FORCE,
        'google_tracking_id': settings.GOOGLE_TRACKING_ID,
        'test_net': settings.TEST_NET,
        'wallet_url': settings.WALLET_URL,
        'burst_info': {
            'exchange': get_exchange_info(),
        }
    }
