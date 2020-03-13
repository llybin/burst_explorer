from java_wallet.models import Account
from scan.caching_data.base import CachingDataBase


class CachingTotalAccountsCount(CachingDataBase):
    _cache_key = "total_accounts_count"
    _cache_expiring = 3600
    live_if_empty = True
    default_data_if_empty = 0

    def _get_live_data(self):
        return (
            Account.objects.using("java_wallet")
            .filter(latest=True)
            .exclude(id=0)
            .count()
        )
