from django.conf import settings

from config import celery_app
from scan.caching_data.exchange import CachingExchangeData
from scan.caching_data.pending_txs import CachingPendingTxs
from scan.caching_data.total_accounts_count import CachingTotalAccountsCount
from scan.caching_data.total_burst_circulation import CachingTotalBurstCirculation
from scan.caching_data.total_multiout_count import CachingTotalMultioutCount
from scan.caching_data.total_txs_count import CachingTotalTxsCount


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    if not settings.TEST_NET:
        sender.add_periodic_task(60, update_cache_exchange_data)

    sender.add_periodic_task(10, update_cache_pending_txs)

    sender.add_periodic_task(3000, update_cache_total_txs_count)
    update_cache_total_txs_count.apply_async(countdown=15)

    sender.add_periodic_task(3200, update_cache_total_multiout_count)
    update_cache_total_multiout_count.apply_async(countdown=30)

    sender.add_periodic_task(3300, update_cache_total_accounts_count)
    update_cache_total_accounts_count.apply_async(countdown=45)

    sender.add_periodic_task(43200, update_cache_total_burst_circulation)
    update_cache_total_burst_circulation.apply_async(countdown=60)


@celery_app.task(time_limit=10)
def update_cache_exchange_data():
    CachingExchangeData().update_live_data()


@celery_app.task(time_limit=10)
def update_cache_pending_txs():
    CachingPendingTxs().update_live_data()


@celery_app.task(time_limit=15)
def update_cache_total_txs_count():
    CachingTotalTxsCount().update_live_data()


@celery_app.task(time_limit=15)
def update_cache_total_multiout_count():
    CachingTotalMultioutCount().update_live_data()


@celery_app.task(time_limit=15)
def update_cache_total_burst_circulation():
    CachingTotalBurstCirculation().update_live_data()


@celery_app.task(time_limit=15)
def update_cache_total_accounts_count():
    CachingTotalAccountsCount().update_live_data()
