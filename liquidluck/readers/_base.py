# coding: utf-8
"""
    liquidluck._base
    ~~~~~~~~~~~~~~~~

    Shared base for readers.

    :copyright: (c) 2013 by Hsiaoming Yang
"""

import re
import os
import datetime
import logging
import hashlib
from .._compat import to_datetime, to_unicode

logger = logging.getLogger('liquidluck')


class Author(object):
    def __init__(self, author, config=None):
        self.author = author
        self._config = config


class Post(object):
    def __init__(self, source, filepath, content, meta=None, config=None):
        self._source = source
        self._config = config

        self.filepath = filepath
        self.content = content
        if not meta:
            meta = {}

        if 'title' in meta:
            self.title = meta.pop('title')
        else:
            self.title = ''
        self.meta = meta

    @property
    def relative_filepath(self):
        if self._source in self.filepath:
            return os.path.relpath(self.filepath, self._source)
        return self.filepath

    @property
    def clean_title(self):
        """Remove useless symbols from title."""
        #: https://github.com/lepture/liquidluck/issues/32
        if not self.title:
            return ''
        title = re.sub(
            r'[<>,~!#&\{\}\(\)\[\]\.\*\^\$\?]', ' ', self.title
        )
        return '-'.join(title.strip().split())

    @property
    def updated(self):
        if not os.path.exists(self.filepath):
            return None
        mtime = os.stat(self.filepath).st_mtime
        return datetime.datetime.fromtimestamp(mtime)

    @property
    def date(self):
        date = self.meta.get('date')
        if not date:
            return None
        return to_datetime(date)

    @property
    def public(self):
        if 'status' in self.meta:
            return self.meta['status'] == 'public'
        return self.meta.get('public', 'true') == 'true'

    @property
    def template(self):
        return self.meta.get('template', None)

    @property
    def category(self):
        return self.meta.get('category', None)

    @property
    def tags(self):
        tags = self.meta.get('tags', None)
        if not tags:
            return []
        if isinstance(tags, (list, tuple)):
            return tags
        return [tag.strip() for tag in tags.split(",")]


class CachedItem(object):
    """A cached item for index."""
    def __init__(self, cache, meta):
        self._cache = cache
        self.meta = meta

    @property
    def content(self):
        if hasattr(self, '_content'):
            return self._content
        post = self._cache.get(self.key)
        return post.content

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            try:
                return self.meta.get(key)
            except ValueError:
                raise AttributeError('No such attribute: %s' % key)

    def __getitem__(self, key):
        return self.meta.get(key)

    def keys(self):
        return self.meta.keys()


class BaseReader(object):
    filetypes = []
    post_class = Post

    def __init__(self, source, cache=None, config=None):
        self._source = source
        self._cache = cache
        self._config = config

    def support(self, filepath):
        """Detect if the reader supports this file."""
        extname = os.path.splitext(filepath)[1]
        return extname[1:] in self.filetypes

    def load(self, filepath):
        """Loading post from a cache."""
        if not self._cache:
            return self.read(filepath)
        key = hashlib.md5(filepath).hexdigest()
        ret = self._cache.get(key)
        if ret:
            return ret
        ret = self.read(filepath)
        if not ret:
            return None
        self._cache.set(key, ret)
        return ret

    def read(self, filepath):
        """Read and parse from a filepath."""
        logger.debug('read %s', filepath)
        if not self.support(filepath):
            logger.debug('%s is not supported', filepath)
            return

        with open(filepath) as f:
            text = to_unicode(f.read())
            content, meta = self.parse(text)
            post = self.post_class(
                source=self._source,
                filepath=filepath,
                content=content,
                meta=meta,
                config=self._config
            )
            return post

    def parse(self, text):
        raise NotImplementedError
