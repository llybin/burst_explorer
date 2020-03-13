from java_wallet.models import Transaction
from scan.caching_data.base import CachingDataBase


class CachingTotalTxsCount(CachingDataBase):
    _cache_key = "total_txs_count"
    _cache_expiring = 3600
    live_if_empty = True
    default_data_if_empty = 0

    def _get_live_data(self):
        return Transaction.objects.using("java_wallet").count()
