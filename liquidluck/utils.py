#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Temp(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError


class Pagination(object):
    def __init__(self, rsts, perpage=30):
        self.allrsts = [rst for rst in rsts]
        self.total = len(self.allrsts)
        self.pages = (self.total - 1)/perpage + 1
        self.perpage = perpage

    def get_current_page(self, page=1):
        start = (page-1) * self.perpage
        end = page * self.perpage
        self.rsts = self.allrsts[start:end]
        if page < self.pages:
            self.next = str(page + 1)
        else:
            self.next = None
        if page > 1:
            self.prev = str(page - 1)
        else:
            self.prev = None
        self.page = page
        return self


def xmldatetime(value):
    """ this is a jinja filter """
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')

def content_url(self, a, *args):
    """ jinja filter """
    path = os.path.join(a, *args)
    path = '{0}/'.format(path.rstrip('/'))
    if not path.startswith('http://'):
        path = '/{0}'.format(path.lstrip('/'))
    return path

class Cache(object):
    def __init__(self):
        self._app_cache = {}

    def set(self, key, value):
        self._app_cache[key] = value

    def get(self, key):
        value = self._app_cache.get(key, None)
        return value

    def delete(self, key):
        if self._app_cache.has_key(key):
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
        for k,v in li:
            store = cache.get(k)
            if not store:
                store = []
            store.append(v)
            cache.set(k, store)
    except:
        pass
    return cache()



def import_module(module):
    parts = module.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1])
