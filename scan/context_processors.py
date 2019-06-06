from django.conf import settings

from scan.information import get_exchange_info


def settings_context_processor(request):
    return {
        'account_name_force': settings.ACCOUNTS_NAME_FORCE,
        'google_tracking_id': settings.GOOGLE_TRACKING_ID,
        'burst_info': {
            'exchange': get_exchange_info(),
        }
    }
