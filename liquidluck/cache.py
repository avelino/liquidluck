# coding: utf-8
"""
    liquidluck.cache
    ~~~~~~~~~~~~~~~~

    Cache system for liquidluck.

    :copyright: (c) 2013 by Hsiaoming Yang
"""

import os
import time
import shutil
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Cache(object):
    """Cache for storing data.

    :param cachedir: where to storing the data, if no value passed,
                     use memory.
    """

    def __init__(self, cachedir=None):
        if cachedir and not os.path.exists(cachedir):
            os.makedirs(cachedir)
        self._cachedir = cachedir
        self._memcache = {}

    def has(self, key):
        """Detecting if the cache exists.

        :param key: key of the cache.
        """
        if not self._cachedir:
            return key in self._memcache
        return os.path.exists(os.path.join(self._cachedir, key))

    def get(self, key):
        """Get the data with the given key.

        :param key: key of the cache.
        """
        if not self._cachedir:
            item = self._memcache.get(key)
            if not item:
                return None
            return item[0]
        cachefile = os.path.join(self._cachedir, key)
        if not os.path.exists(cachefile):
            return None
        with open(cachefile) as f:
            return pickle.load(f)

    def set(self, key, value):
        """Storing the data with the given key.

        :param key: key of the cache.
        :param value: data to be stored in the cache.
        """
        if not self._cachedir:
            self._memcache[key] = (value, time.time())
            return self
        cachefile = os.path.join(self._cachedir, key)
        with open(cachefile, 'wb') as f:
            pickle.dump(value, f)
            return self

    def clear(self, key):
        """Delete the cache data with the given key.

        :param key: key of the cache.
        """
        if not self._cachedir:
            if key in self._memcache:
                return self._memcache.pop(key)

        cachefile = os.path.join(self._cachedir, key)
        if os.path.exists(cachefile):
            os.remove(cachefile)

    def flush(self):
        """Flush all cache data."""
        if not self._cachedir:
            self._memcache = {}
        elif os.path.exists(self._cachedir):
            shutil.rmtree(self._cachedir)

    def mtime(self, key):
        """Modified time for the cache of the given key."""
        if not self._cachedir:
            item = self._memcache.get(key)
            if not item:
                return None
            return item[1]
        cachefile = os.path.join(self._cachedir, key)
        if os.path.exists(cachefile):
            return os.stat(cachefile).st_mtime
        return None
