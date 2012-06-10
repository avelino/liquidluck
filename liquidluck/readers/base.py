#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Reader, read content, parse to html.

:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''

import datetime
import logging
from liquidluck.options import settings
from liquidluck.utils import import_module


class BaseReader(object):
    """
    Base Reader, all readers must inherit this module. e.g.:

        ``MarkdownReader(BaseReader)``

    New reader required:
        - ``support_type``
        - ``render``

    New reader optional:
        - ``start``
    """
    def __init__(self, filepath=None):
        self.filepath = filepath

    def start(self):
        return None

    def support_type(self):
        return None

    def support(self):
        _type = self.support_type()
        if isinstance(_type, basestring):
            return self.filepath.endswith('.' + _type)
        if isinstance(_type, list) or isinstance(_type, tuple):
            for _t in _type:
                if isinstance(_t, basestring) and \
                   self.filepath.endswith('.' + _t):
                    return True
        return False

    def render(self):
        raise NotImplementedError


class Post(object):
    meta = {}

    def __init__(self, filepath, content, title=None, meta=None):
        self.filepath = filepath
        self.content = content
        if title:
            self.title = title
        else:
            self.title = meta.pop('title')

        if meta:
            self.meta = meta

    @property
    def author(self):
        return self.meta.get('author', settings.author)

    @property
    def date(self):
        date = self.meta.get('date', None)
        if date:
            return to_datetime(date)
        return None

    @property
    def public(self):
        return self.meta.get('public', 'true') == 'true'

    @property
    def folder(self):
        return self.meta.get('folder', None)

    @property
    def tags(self):
        tags = self.meta.get('tags', None)
        if not tags:
            return []
        if isinstance(tags, (list, tuple)):
            return tags
        return [tag.strip() for tag in tags.split(",")]


def to_datetime(value):
    supported_formats = [
        '%a %b %d %H:%M:%S %Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%dT%H:%M',
        '%Y%m%d %H:%M:%S',
        '%Y%m%d %H:%M',
        '%Y-%m-%d',
        '%Y%m%d',
    ]
    for format in supported_formats:
        try:
            return datetime.datetime.strptime(value, format)
        except ValueError:
            pass
    logging.error('Unrecognized date/time: %r' % value)
    raise ValueError('Unrecognized date/time: %r' % value)


def detect_reader(filepath):
    for reader in settings.readers.values():
        reader = import_module(reader)(filepath)
        if reader.support():
            return reader
    return None
