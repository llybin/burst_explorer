from abc import ABC, abstractmethod
from typing import Any

from django.core.cache import cache


class CachingDataBase(ABC):
    @property
    @abstractmethod
    def _cache_key(self) -> str:
        pass

    @property
    @abstractmethod
    def _cache_expiring(self) -> int:
        pass

    @property
    @abstractmethod
    def live_if_empty(self) -> bool:
        pass

    @property
    @abstractmethod
    def default_data_if_empty(self) -> Any:
        pass

    @abstractmethod
    def _get_live_data(self):
        pass

    @property
    def live_data(self):
        return self._get_live_data()

    def _get_cached_data(self):
        data = cache.get(self._get_cache_key())
        if data:
            data = self._loads(data)
        else:
            if self.live_if_empty:
                data = self.live_data
        return data or self.default_data_if_empty

    @property
    def cached_data(self):
        return self._get_cached_data()

    def _loads(self, data):
        return data

    def _dumps(self, data):
        return data

    def _get_cache_key(self):
        return f"caching_data:{self._cache_key}"

    def update_data(self, data):
        cache.set(self._get_cache_key(), self._dumps(data), self._cache_expiring)

    def clear_cached_data(self):
        cache.delete(self._get_cache_key())

    def update_live_data(self):
        self.update_data(self.live_data)
