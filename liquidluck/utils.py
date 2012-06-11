#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    return value


def utf8(value):
    if isinstance(value, (bytes, type(None))):
        return value
    return value.encode('utf-8')


def import_object(name):
    if '.' not in name:
        return __import__(name)

    parts = name.split('.')
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
            return None

    def __setattr__(self, key, value):
        self[key] = to_unicode(value)

    def __getitem__(self, key):
        return to_unicode(super(UnicodeDict, self).__getitem__(key))

    def __setitem__(self, key, value):
        return super(UnicodeDict, self).__setitem__(key, to_unicode(value))
