from mako.cache import CacheImpl, register_plugin
from django.core.cache import cache

class DjangoCache(CacheImpl):
    def __init__(self, cache):
        super(DjangoCache, self).__init__(cache)

    def get_or_create(self, key, creation_function, **kw):
        value = cache.get(key)

        if not value:
            timeout = kw.get('timeout', None)
            value = creation_function()
            cache.set(key, value, timeout)

        return value

    def set(self, key, value, **kwargs):
        timeout = kw.get('timeout', None)
        cache.set(key, value, timeout)

    def get(self, key, **kwargs):
        return cache.get(key)

    def invalidate(self, key, **kwargs):
        cache.delete(key)

# optional - register the class locally
register_plugin("django_cache", __name__, "DjangoCache")