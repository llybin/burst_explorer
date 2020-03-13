from java_wallet.models import Block
from scan.caching_data.base import CachingDataBase


class CachingLastHeight(CachingDataBase):
    _cache_key = "last_height"
    _cache_expiring = 0
    live_if_empty = True
    default_data_if_empty = None

    def _get_live_data(self):
        return (
            Block.objects.using("java_wallet")
            .order_by("-height")
            .values_list("height", flat=True)
            .first()
        )
