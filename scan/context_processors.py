from django.conf import settings


def settings_context_processor(request):
    return {
        'ACCOUNTS_NAME_FORCE': settings.ACCOUNTS_NAME_FORCE,
    }
