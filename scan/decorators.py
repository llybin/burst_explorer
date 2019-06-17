from functools import wraps

from django.core.cache import cache


def lock_decorator(key=None, expire=None, ident=None, auto_renewal=False):
    def decorator(func):
        def _make_lock_key():
            return "lock_decorator:{}".format(key or func.__name__)

        @wraps(func)
        def inner(*args, **kwargs):
            lock_key = _make_lock_key()
            with cache.lock(lock_key, expire, ident, auto_renewal):
                return func(*args, **kwargs)

        return inner

    return decorator
