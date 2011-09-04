#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from fnmatch import fnmatch
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import Environment, FileSystemLoader, Markup
from reader import rstReader

import log


builtin_templates = os.path.join(os.path.dirname(__file__), 'templates')

def sort_rsts(rsts, reverse=True):
    return sorted(rsts, key=lambda rst: rst.get_info('date'), reverse=reverse)

class Walker(object):
    def __init__(self, config, projectdir):
        self.config = config
        self.projectdir = projectdir

    @property
    def postdir(self):
        _dir = self.config.get('postdir', 'content')
        return os.path.join(self.projectdir, _dir)

    @property
    def deploydir(self):
        _dir = self.config.get('deploydir', 'deploy')
        return os.path.join(self.projectdir, _dir)

    def walk(self):
        for root, dirs, files in os.walk(self.postdir):
            for f in files:
                path = os.path.join(root, f)
                rst = rstReader(path)
                yield rst

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


    def mkdir_dest_folder(self, dest):
        folder = os.path.split(dest)[0]
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return folder

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

    def write_archive(self, rsts, dest='archive.html'):
        dest = os.path.join(self.deploydir, dest)
        self.mkdir_dest_folder(dest)

        f = open(dest, 'w')
        _tpl = self.config.get('archive_template', 'archive.html')
        html = self._jinja_render(_tpl, {'rsts': rsts})
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

    def _jinja_render(self, template, context={}):
        prepare = {'site': self.config.site, 'context': self.config.context}
        context.update(prepare)
        tpl = self.jinja.get_template(template)
        return tpl.render(context)

    def run(self):
        rsts = sort_rsts(self.walk())
        for rst in self._calc_single_posts(rsts):
            self.write_post(rst)

        for k,v in merge(self._calc_folder_posts(rsts)).iteritems():
            dest = os.path.join(k, 'index.html')
            self.write_archive(v, dest)
            dest = os.path.join(k, 'feed.xml')
            self.write_feed(v, dest)

        for k, v in merge(self._calc_year_posts(rsts)).iteritems():
            dest = os.path.join(str(k), 'index.html')
            self.write_archive(v, dest)
            dest = os.path.join(str(k), 'feed.xml')
            self.write_feed(v, dest)

        for k, v in merge(self._calc_tag_posts(rsts)).iteritems():
            dest = os.path.join('tag', k + '.html')
            self.write_archive(v, dest)

        archives = self._calc_archive_posts(rsts)
        self.write_archive(archives, 'archive.html')
        self.write_feed(archives, 'feed.xml')

        log.info('finished')
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
