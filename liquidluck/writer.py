#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from math import log
from fnmatch import fnmatch
import shutil
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import Environment, FileSystemLoader, Markup
from reader import rstReader
from config import Temp

import logger


builtin_templates = os.path.join(os.path.dirname(__file__), 'templates')

def sort_rsts(rsts, reverse=True):
    return sorted(rsts, key=lambda rst: rst.get_info('date'), reverse=reverse)

class Walker(object):
    _cache = []

    def __init__(self, config, projectdir):
        self.config = config
        self.projectdir = projectdir

    def mkdir_dest_folder(self, dest):
        folder = os.path.split(dest)[0]
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return folder

    @property
    def postdir(self):
        _dir = self.config.get('postdir', 'content')
        return os.path.join(self.projectdir, _dir)

    @property
    def deploydir(self):
        _dir = self.config.get('deploydir', 'deploy')
        return os.path.join(self.projectdir, _dir)

    @property
    def ignore(self):
        return self.config.get('ignore', 'tmp/*').split()

    def static_url(self, name):
        f = os.path.join(self.config.get('staticdir', '_static'), name)
        url = self.config.get('static_prefix', '/static')
        stat = int(os.stat(f).st_mtime)

        if f not in self._cache:
            folder = os.path.join(self.deploydir, '_static')
            if not os.path.isdir(folder):
                os.makedirs(folder)
            shutil.copy(f, folder)
            self._cache.append(f)
            logger.info('copy ' + f)

        return os.path.join(url, name) + '?t=' + str(stat)

    def walk(self):
        for root, dirs, files in os.walk(self.postdir):
            for f in files:
                path = os.path.join(root, f)
                if any([fnmatch(path, pattern) for pattern in self.ignore]):
                    logger.warn('ignore file: ' + path)
                elif path.endswith('.rst'):
                    rst = rstReader(path)
                    yield rst
                else:
                    dest = os.path.join(
                        self.deploydir,
                        path.replace(self.postdir,'').lstrip('/')
                    )
                    self.mkdir_dest_folder(dest)
                    shutil.copy(path, dest)
                    #TODO

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

class Writer(Walker):
    def __init__(self, config, projectdir):
        super(Writer, self).__init__(config, projectdir)

        tpl = os.path.join(projectdir, config.site.get('template', 'templates'))
        self.jinja = Environment(
            loader = FileSystemLoader([tpl, builtin_templates]),
            autoescape = config.site.get('autoescape', False),
            extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        )

    def write_post(self, rst):
        public = rst.get_info('public', 'true')
        if 'false' == public.lower():
            return # this is a secret post

        dest = os.path.join(self.deploydir, rst.destination)
        self.mkdir_dest_folder(dest)

        f = open(dest, 'w')
        _tpl = rst.get_info('tpl', 'post.html')
        html = self._jinja_render(_tpl, {'rst': rst})
        f.write(html)
        f.close()
        return 

    def write_archive(self, rsts, title='Archive', dest='archive.html'):
        dest = os.path.join(self.deploydir, dest)
        self.mkdir_dest_folder(dest)

        f = open(dest, 'w')
        _tpl = self.config.get('archive_template', 'archive.html')
        html = self._jinja_render(_tpl, {'title': title, 'rsts': rsts})
        f.write(html)
        f.close()
        return 

    def write_feed(self, rsts, dest='feed.xml'):
        dest = os.path.join(self.deploydir, dest)
        self.mkdir_dest_folder(dest)

        f = open(dest, 'w')
        _tpl = self.config.get('feed_template', 'feed.xml')
        html = self._jinja_render(_tpl, {'rsts': rsts})
        f.write(html)
        f.close()
        return 

    def write_tagcloud(self, tagcloud):
        dest = os.path.join(self.deploydir, 'tag/index.html')
        self.mkdir_dest_folder(dest)

        tags = []
        for k, v in tagcloud.iteritems():
            tag = Temp()
            tag.name = k
            tag.count = len(v)
            tag.size = 100 + log(tag.count or 1)*20
            tags.append(tag)

        f = open(dest, 'w')
        _tpl = self.config.get('tagcloud_template', 'tagcloud.html')
        html = self._jinja_render(_tpl, {'tags': tags})
        f.write(html)
        f.close()
        return 

    def _jinja_render(self, template, context={}):
        prepare = {}
        prepare['context'] = self.config.context
        prepare['static_url' ] = self.static_url
        context.update(prepare)
        tpl = self.jinja.get_template(template)
        return tpl.render(context)

    def run(self):
        rsts = sort_rsts(self.walk())
        print rsts
        for rst in self._calc_single_posts(rsts):
            self.write_post(rst)

        for k,v in merge(self._calc_folder_posts(rsts)).iteritems():
            dest = os.path.join(k, 'index.html')
            self.write_archive(v, k, dest)
            dest = os.path.join(k, 'feed.xml')
            self.write_feed(v, dest)

        for k, v in merge(self._calc_year_posts(rsts)).iteritems():
            dest = os.path.join(str(k), 'index.html')
            self.write_archive(v, k, dest)
            dest = os.path.join(str(k), 'feed.xml')
            self.write_feed(v, dest)

        tagcloud = merge(self._calc_tag_posts(rsts))
        for k, v in tagcloud.iteritems():
            dest = os.path.join('tag', k + '.html')
            self.write_archive(v, k, dest)
        self.write_tagcloud(tagcloud)

        archives = self._calc_archive_posts(rsts)
        self.write_archive(archives)
        self.write_feed(archives, 'feed.xml')

        logger.info('finished')
        return

    def _calc_archive_posts(self, rsts):
        for rst in rsts:
            public = rst.get_info('public', True)
            if public:
                yield rst

    def _calc_single_posts(self, rsts):
        i = 0
        for rst in self._calc_archive_posts(rsts):
            if i > 0:
                rst.prev = rsts[i-1]
            i += 1
            if i < len(rsts):
                rst.next = rsts[i]
            yield rst

    def _calc_folder_posts(self, rsts):
        for rst in self._calc_archive_posts(rsts):
            folder = rst.get_info('folder')
            if folder:
                yield folder, rst

    def _calc_year_posts(self, rsts):
        for rst in self._calc_archive_posts(rsts):
            date = rst.get_info('date')
            yield date.year, rst

    def _calc_tag_posts(self, rsts):
        for rst in self._calc_archive_posts(rsts):
            tags = rst.get_info('tags')
            for tag in tags:
                yield tag, rst
