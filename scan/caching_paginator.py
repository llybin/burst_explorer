from django.core.cache import cache
from django.core.paginator import Paginator


class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            key = f"paginator:{hash(self.object_list.query.__str__())}:count"
            self._count = cache.get(key, -1)
            if self._count == -1:
                self._count = super().count
                cache.set(key, self._count, 3600)

        return self._count

    count = property(_get_count)
