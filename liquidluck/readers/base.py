#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Reader, read content, parse to html.

:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''

import os
import logging
import datetime
import re
from liquidluck.options import settings, g
from liquidluck.utils import to_datetime, import_object


class BaseReader(object):
    SUPPORT_TYPE = None
    """
    Base Reader, all readers must inherit this module. e.g.:

        ``MarkdownReader(BaseReader)``

    New reader required:
        - ``SUPPORT_TYPE``
        - ``render``

    New reader optional:
        - ``start``
    """
    def __init__(self, filepath=None):
        self.filepath = filepath

    @property
    def relative_filepath(self):
        return self.filepath[len(g.source_directory) + 1:]

    def start(self):
        return None

    def support(self):
        _type = self.SUPPORT_TYPE
        if isinstance(_type, basestring):
            return self.filepath.endswith('.' + _type)
        if isinstance(_type, list) or isinstance(_type, tuple):
            for _t in _type:
                if isinstance(_t, basestring) and \
                   self.filepath.endswith('.' + _t):
                    return True
        return False

    def get(self, key, value=None):
        variables = settings.reader.get('vars') or {}
        return variables.get(key, value)

    @property
    def post_class(self):
        cls = self.get('post_class', Post)
        if isinstance(cls, str):
            return import_object(cls)
        return cls

    def render(self):
        raise NotImplementedError

    def run(self):
        try:
            return self.render()
        except Exception as e:
            logging.error(e)
            if g.interrupt:
                raise e


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
    def clean_title(self):
        #: https://github.com/lepture/liquidluck/issues/32
        title = re.sub(
            r'[<>,~!#&\{\}\(\)\[\]\.\*\^\$\?]', ' ', self.title
        )
        return '-'.join(title.strip().split())

    @property
    def author(self):
        author = settings.author.get('default', 'admin')
        return Author(self.meta.get('author', author))

    @property
    def embed_author(self):
        """define in settings::

            authors = {
                "lepture": {
                    "name": "Hsiaoming Yang",
                    "website": "http://lepture.com",
                    "email": "lepture@me.com",
                }
            }
        """
        author = self.author
        if author.website:
            return '<a href="%s">%s</a>' % (author.website, author.name)
        if author.email:
            return '<a href="mailto:%s">%s</a>' % (author.email, author.name)
        return author.name

    @property
    def date(self):
        return to_datetime(self.meta.get('date'))

    @property
    def updated(self):
        mtime = os.stat(self.filepath).st_mtime
        return datetime.datetime.fromtimestamp(mtime)

    @property
    def public(self):
        return self.meta.get('public', 'true') == 'true'

    @property
    def category(self):
        category = self.meta.get('category', None)
        if category:
            return category
        #: historical reason
        return self.meta.get('folder', None)

    @property
    def tags(self):
        tags = self.meta.get('tags', None)
        if not tags:
            return []
        if isinstance(tags, (list, tuple)):
            return tags
        return [tag.strip() for tag in tags.split(",")]

    @property
    def summary(self):
        return self.meta.get('summary', None)

    @property
    def template(self):
        return self.meta.get('template', None)

    @property
    def filename(self):
        if self.meta.get('filename'):
            return self.meta.get('filename')
        path = os.path.split(self.filepath)[1]
        return os.path.splitext(path)[0]

    @property
    def clean_filepath(self):
        path = self.filepath
        if path.startswith(g.source_directory):
            return path[len(g.source_directory) + 1:]
        return path

    @property
    def clean_folder(self):
        return os.path.split(self.clean_filepath)[0]

    def __getattr__(self, key):
        try:
            return super(Post, self).__getattr__(key)
        except:
            pass
        #: won't raise AttributeError
        return self.meta.get(key)


class Author(object):
    def __init__(self, author):
        self.author = author

        __ = settings.author.get('vars') or {}
        self._d = __.get(author, {})

    def __str__(self):
        return self.author

    def __repr__(self):
        return self.author

    @property
    def name(self):
        return self._d.get('name', self.author)

    @property
    def website(self):
        return self._d.get('website', None)

    @property
    def email(self):
        return self._d.get('email', None)
