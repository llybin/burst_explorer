from django.conf import settings

from config import celery_app
from scan.helpers.exchange import get_exchange_data, set_cache_exchange_data


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    if not settings.TEST_NET:
        sender.add_periodic_task(60, get_exchange_info)


@celery_app.task(time_limit=10)
def get_exchange_info():
    data = get_exchange_data()
    set_cache_exchange_data(data)
