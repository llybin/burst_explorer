from config import celery_app
from scan.helpers.exchange import cache_exchange_data, get_exchange_data


@celery_app.task(time_limit=5)
def get_exchange_info():
    data = get_exchange_data()
    cache_exchange_data(data)
