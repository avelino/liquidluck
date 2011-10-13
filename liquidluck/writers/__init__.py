
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Writer, write your content to html.

:copyright: (c) 2011 by Hsiaoming Young (aka lepture)
:license: BSD
'''


import os
import datetime
import shutil
from fnmatch import fnmatch
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import Environment, FileSystemLoader

from liquidluck.readers.rst import restructuredtext
from liquidluck.utils import Pagination
from liquidluck.utils import xmldatetime
from liquidluck.utils import import_module

from liquidluck import logger

_total_posts = []
_not_posts = []

class Writer(object):
    _jinja_context = {}
    _jinja_filters = {}

    def __init__(self, config, projectdir):
        self.config = config
        self.projectdir = projectdir

        tpl = os.path.join(projectdir, config.site.get('template', 'templates'))
        self.jinja = Environment(
            loader = FileSystemLoader([tpl]),
            autoescape = config.site.get('autoescape', False),
            extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        )

        #init
        self.register_context('context', self.config.context)
        self.register_context('now', datetime.datetime.now())

        for k, v in config.filters.items():
            if k not in self._jinja_filters:
                logger.info('Register filter: %s' % v)
                self.register_filter(k, import_module(v))

    def reader(self):
        if hasattr(self, '_reader'):
            return self._reader
        reader = self.config.get('reader', 'liquidluck.readers.rst.RstReader')
        logger.info('Apply Reader: %s' % reader)
        self._reader = import_module(reader)
        return self._reader

    @property
    def postdir(self):
        _dir = self.config.get('postdir', 'content')
        return os.path.join(self.projectdir, _dir)

    @property
    def deploydir(self):
        _dir = self.config.get('deploydir', 'deploy')
        return os.path.join(self.projectdir, _dir)

    @property
    def staticdir(self):
        _dir = self.config.get('staticdir', '_static')
        return os.path.join(self.projectdir, _dir)

    @property
    def total_files(self):
        global _total_posts
        global _not_posts
        if _total_posts or _not_posts:
            return _total_posts, _not_posts
        for f in self.walk(self.postdir):
            reader = self.reader()
            parsed = reader(f, self.config)
            if parsed.support():
                _total_posts.append(parsed.render())
            else:
                _not_posts.append(f)
        return _total_posts, _not_posts

    @classmethod
    def register_context(cls, key, value):
        cls._jinja_context[key] = value
        return cls

    @classmethod
    def register_filter(cls, key, value):
        if key not in cls._jinja_filters:
            cls._jinja_filters[key] = value
        return cls

    def render(self, template, context={}):
        context.update(self._jinja_context)
        self.jinja.filters.update(self._jinja_filters)
        tpl = self.jinja.get_template(template)
        return tpl.render(context)


    def make_dest_folder(self, dest):
        folder = os.path.split(dest)[0]
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return folder

    def copy_to(self, source, dest):
        if os.path.exists(dest) and os.stat(source).st_mtime < os.stat(dest).st_mtime:
            logger.info('Ignore ' + source)
            return False
        self.make_dest_folder(dest)
        logger.info('copy ' + source)
        shutil.copy(source, dest)
        return True

    def sort_posts(self, posts, reverse=True):
        return sorted(posts, key=lambda post: post.date, reverse=reverse)

    def walk(self, dest):
        for root, dirs, files in os.walk(dest):
            for f in files:
                path = os.path.join(root, f)
                yield path
    
    def write(self, params, tpl, dest):
        dest = os.path.join(self.deploydir, dest)
        logger.info('write ' + dest)
        self.make_dest_folder(dest)
        f = open(dest, 'w')
        html = self.render(tpl, params)
        f.write(html.encode('utf-8'))
        f.close()
        return 

    def register(self):
        pass

    def run(self):
        pass


class ArchiveMixin(object):
    def calc_archive_posts(self):
        for post in self.total_files[0]:
            if post.public:
                yield post

class FeedMixin(object):
    def write_feed(self, posts, dest='feed.xml'):
        count = int(self.config.get('feed_count',10))
        posts = posts[:count]
        _tpl = self.config.get('feed_template', 'feed.xml')
        return self.write({'posts':posts}, _tpl, dest)

    def register(self):
        self.register_filter('xmldatetime', xmldatetime)

class PagerMixin(object):
    def write_pager(self, posts, dest='archive.html'):
        perpage = int(self.config.get('perpage', 30))
        paginator = Pagination(posts, perpage)
        _tpl = self.config.get('archive_template', 'archive.html')

        # first page
        folder, filename = os.path.split(dest)

        pager = paginator.get_current_page(1)
        pager.folder = folder

        self.write({'pager': pager}, _tpl, dest)

        for p in range(paginator.pages):
            dest = os.path.join(folder, 'page', '{0}.html'.format(p+1))
            pager = paginator.get_current_page(p+1)
            pager.folder = folder
            self.write({'pager': pager}, _tpl, dest)


