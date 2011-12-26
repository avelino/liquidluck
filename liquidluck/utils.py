#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Cache(object):
    def __init__(self):
        self._app_cache = {}

    def set(self, key, value):
        self._app_cache[key] = value

    def get(self, key):
        value = self._app_cache.get(key, None)
        return value

    def delete(self, key):
        if key in self._app_cache:
            del self._app_cache[key]
        return None

    def __call__(self):
        return self._app_cache


def merge(li):
    '''
    [(a,b),(a,c),(a,d)] -> {a:[b,c,d]}
    '''
    cache = Cache()
    try:
        for k, v in li:
            store = cache.get(k)
            if not store:
                store = []
            store.append(v)
            cache.set(k, store)
    except:
        pass
    return cache()


def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    return value


def import_module(module):
    parts = module.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1])


def walk_dir(dest):
    for root, dirs, files in os.walk(dest):
        for f in files:
            path = os.path.join(root, f)
            yield path


class UnicodeDict(dict):
    def __getattr__(self, key):
        try:
            return to_unicode(self[key])
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = to_unicode(value)

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def __getitem__(self, key):
        return to_unicode(super(UnicodeDict, self).__getitem__(key))

    def __setitem__(self, key, value):
        return super(UnicodeDict, self).__setitem__(key, to_unicode(value))
