from scan.caching_data.base import CachingDataBase
from scan.models import MultiOut


class CachingTotalMultioutCount(CachingDataBase):
    _cache_key = "total_multiout_count"
    _cache_expiring = 3600
    live_if_empty = True
    default_data_if_empty = 0

    def _get_live_data(self):
        return MultiOut.objects.count()
