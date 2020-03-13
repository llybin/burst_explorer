from django.db.models import Sum

from java_wallet.models import Account
from scan.caching_data.base import CachingDataBase


class CachingTotalBurstCirculation(CachingDataBase):
    _cache_key = "total_burst_circulation"
    _cache_expiring = 86400
    live_if_empty = True
    default_data_if_empty = 0

    def _get_live_data(self):
        # TODO: add delta
        return (
            Account.objects.using("java_wallet")
            .filter(latest=True)
            .exclude(id=0)
            .aggregate(Sum("balance"))["balance__sum"]
        )
