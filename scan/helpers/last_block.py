from django.core.cache import cache

from java_wallet.models import Block

LAST_HEIGHT_CACHE_KEY = "last_height"


def get_cached_last_height() -> int:
    return cache.get(LAST_HEIGHT_CACHE_KEY, 0)


def set_cache_last_height(height: int):
    cache.set(LAST_HEIGHT_CACHE_KEY, height)


def get_last_height() -> int:
    return (
        Block.objects.using("java_wallet")
        .order_by("-height")
        .values_list("height", flat=True)
        .first()
    )
