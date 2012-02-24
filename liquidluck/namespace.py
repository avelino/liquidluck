#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['NameSpace', 'ns']

from .utils import UnicodeDict


class NameSpace(dict):
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

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

ns = NameSpace.instance()


#defaults
ns.storage = NameSpace()
ns.storage.errors = []  # error list storage
ns.storage.status = NameSpace()  # status of the blog info
ns.storage.functions = NameSpace()  # functions storage for writer
ns.storage.root = None
ns.storage.posts = []
ns.storage.files = []


ns.context = UnicodeDict()  # [context] in config file

# [site] in config file
ns.site = NameSpace({
    'postdir': 'content',
    'deploydir': 'deploy',
    'staticdir': 'static',
    'static_prefix': '/static',
    'template': '_templates',
    'format': 'year',
    'slug': 'html',
    'syntax': 'class',
    'autoescape': 'false',
    'feed_count': 10,
    'perpage': 30,
    'index': 'index.html',
    'feed_template': 'feed.xml',
    'archive_template': 'archive.html',
    'tagcloud_template': 'tagcloud.html',
})
# [readers] in config file
ns.readers = NameSpace({
    'mkd': 'liquidluck.readers.mkd.MarkdownReader',
    'rst': 'liquidluck.readers.rst.RstReader',
})
# [writers] in config file
ns.writers = NameSpace({
    'static': 'liquidluck.writers.default.StaticWriter',
    'post': 'liquidluck.writers.default.PostWriter',
    'file': 'liquidluck.writers.default.FileWriter',
    'archive': 'liquidluck.writers.default.IndexWriter',
    'year': 'liquidluck.writers.default.YearWriter',
    'tag': 'liquidluck.writers.default.TagWriter',
})
# [filters] in config file
ns.filters = NameSpace({
    'restructuredtext': 'liquidluck.readers.rst.restructuredtext',
    'markdown': 'liquidluck.readers.mkd.markdown',
    'xmldatetime': 'liquidluck.filters.xmldatetime',
})
# other sections in config file
# ns.sections[section] = sectionData
ns.sections = NameSpace()

# data in sections
# section name: xxx_data
ns.data = NameSpace()
