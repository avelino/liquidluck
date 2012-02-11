#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
from math import log

from liquidluck.writers import Writer, FeedMixin, PagerMixin
from liquidluck.writers import sort_posts, copy_to
from liquidluck.utils import merge, to_unicode, walk_dir
from liquidluck.namespace import ns, NameSpace
from liquidluck import logger

_hash_cache = {}


def static_url(name):
    global _hash_cache
    url = ns.site.static_prefix
    if name in _hash_cache:
        return os.path.join(url, name) + '?v=' + _hash_cache[name]

    f = os.path.join(ns.storage.projectdir,
                     ns.site.staticdir, name)
    if not os.path.exists(f):
        logger.warn('No such static file: %s' % f)
        return os.path.join(url, name)
    f = open(f, 'rb')
    stat = hashlib.md5(f.read()).hexdigest()[:5]
    _hash_cache[name] = stat
    return os.path.join(url, name) + '?v=' + stat


class StaticWriter(Writer):
    writer_type = 'Static Writer'

    def start(self):
        ns.storage.functions.update({'static_url': static_url})
        return

    def run(self):
        for source in walk_dir(self.staticdir):
            path = source.replace(ns.storage.projectdir, '').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            copy_to(source, dest)


def content_url(a, *args):
    slug = ns.site.slug
    args = [to_unicode(arg) for arg in args]
    path = os.path.join(to_unicode(a), *args)
    basename, ext = os.path.splitext(path)
    if not ext:
        path = basename + '/'

    if slug == 'clean':
        path = basename
    if slug == 'slash':
        path = basename + '/'

    if not path.startswith('http://'):
        path = '/%s' % path.lstrip('/')
    return path.lower()


class PostWriter(Writer):
    writer_type = 'Post Writer'

    def start(self):
        return ns.storage.functions.update({'content_url': content_url})

    def _write_post(self, post):
        _tpl = post.get('template', 'post.html')
        self.write({'post': post}, _tpl, post.destination)

    def _get_rel_posts(self, post):
        if not post.public:
            logger.warn('Non-indexed Post: %s' % post.filepath)
            return post
        olders = filter(lambda p: p.date < post.date and p.public,
                       ns.storage.posts)
        newers = filter(lambda p: p.date > post.date and p.public,
                       ns.storage.posts)
        if olders:
            post.older = sort_posts(olders)[0]
        if newers:
            post.newer = sort_posts(newers, False)[0]
        return post

    def run(self):
        for post in ns.storage.posts:
            post = self._get_rel_posts(post)
            self._write_post(post)


class FileWriter(Writer):
    writer_type = 'File Writer'

    def run(self):
        for source in ns.storage.files:
            path = source.replace(self.postdir, '').lstrip('/')
            dest = os.path.join(self.deploydir, path)
            copy_to(source, dest)


class IndexWriter(Writer, PagerMixin, FeedMixin):
    writer_type = 'Index Writer'

    def start(self):
        ns.storage.status.posts = ns.storage.public_posts
        return

    def run(self):
        posts = ns.storage.public_posts
        dest = ns.site.index
        params = {'title': 'Archive'}
        _tpl = ns.site.get('index_archive_template', None)
        if _tpl:
            params.update({'tpl': _tpl})
        self.write_pager(posts, dest, **params)

        params = {'folder': ''}
        _tpl = ns.site.get('index_feed_template', None)
        if _tpl:
            params.update({'tpl': _tpl})
        self.write_feed(posts, dest='feed.xml', **params)


class YearWriter(Writer, PagerMixin, FeedMixin):
    writer_type = 'Year Writer'

    def calc_year_posts(self):
        for post in ns.storage.public_posts:
            yield post.date.year, post

    def start(self):
        ns.storage.status.years = []
        for year, posts in self.calc_year_posts():
            ns.storage.status.years.append(year)
        ns.storage.status.years = sorted(set(ns.storage.status.years))
        return

    def run(self):
        _tpl = ns.site.get('year_archive_template', None)
        for year, posts in merge(self.calc_year_posts()).items():
            posts = sort_posts(posts)
            year = str(year)
            dest = os.path.join(year, 'index.html')
            params = {'title': year}
            if _tpl:
                params.update({'tpl': _tpl})
            self.write_pager(posts, dest, **params)


class TagWriter(Writer, PagerMixin):
    writer_type = 'Tag Writer'

    def calc_tag_posts(self):
        for post in ns.storage.public_posts:
            tags = post.get('tags', [])
            for tag in tags:
                yield tag, post

    def calc_tagcloud(self):
        tagcloud = merge(self.calc_tag_posts())
        for k, v in tagcloud.items():
            tag = NameSpace(
                name=k,
                count=len(v),
                size=100 + log(len(v) or 1) * 20,
            )
            yield tag

    def start(self):
        ns.storage.status.tags = [tag for tag in self.calc_tagcloud()]
        return

    def write_tagcloud(self):
        dest = 'tag/index.html'
        _tpl = ns.site.tagcloud_template
        return self.write({'tags': ns.storage.status.tags}, _tpl, dest)

    def run(self):
        self.write_tagcloud()

        tagcloud = merge(self.calc_tag_posts())
        _tpl = ns.site.get('tag_archive_template', None)
        for tag, posts in tagcloud.items():
            posts = sort_posts(posts)
            dest = os.path.join('tag', tag, 'index.html')
            params = {'title': tag}
            if _tpl:
                params.update({'tpl': _tpl})
            self.write_pager(posts, dest, **params)


class FolderWriter(Writer, PagerMixin, FeedMixin):
    writer_type = 'Folder Writer'

    def calc_folder_posts(self):
        for post in ns.storage.public_posts:
            folder = post.get('folder', None)
            if folder:
                yield folder, post

    def start(self):
        ns.storage.status.folders = []
        for folder, posts in self.calc_folder_posts():
            ns.storage.status.folders.append(folder)
        ns.storage.status.folders = set(ns.storage.status.folders)
        return

    def run(self):
        _archive_tpl = ns.site.get('folder_archive_template', None)
        _feed_tpl = ns.site.get('folder_feed_template', None)
        for folder, posts in merge(self.calc_folder_posts()).iteritems():
            posts = sort_posts(posts)
            dest = os.path.join(folder, 'index.html')
            params = {'title': folder, 'folder': folder}
            if _archive_tpl:
                params.update({'tpl': _archive_tpl})
            self.write_pager(posts, dest, **params)

            dest = os.path.join(folder, 'feed.xml')
            params = {'title': folder, 'folder': folder}
            if _feed_tpl:
                params.update({'tpl': _feed_tpl})
            self.write_feed(posts, dest, **params)


class CategoryWriter(Writer, PagerMixin, FeedMixin):
    writer_type = 'Category Writer'

    def calc_category_posts(self):
        key = ns.site.get('category', 'category')
        for post in ns.storage.public_posts:
            category = post.get(key, None)
            if category:
                yield category, post

    def start(self):
        ns.storage.status.categories = []
        for cat, posts in self.calc_category_posts():
            ns.storage.status.categories.append(cat)
        ns.storage.status.categories = set(ns.storage.status.categories)
        return

    def run(self):
        key = ns.site.get('category', 'category')
        _archive_tpl = ns.site.get('category_archive_template', None)
        _feed_tpl = ns.site.get('category_feed_template', None)
        for cat, posts in merge(self.calc_category_posts()).iteritems():
            posts = sort_posts(posts)
            dest = os.path.join(key, cat, 'index.html')
            params = {'title': cat}
            if _archive_tpl:
                params.update({'tpl': _archive_tpl})
            self.write_pager(posts, dest, **params)
            dest = os.path.join(key, cat, 'feed.xml')
            params = {'title': cat, 'folder': ''}
            if _feed_tpl:
                params.update({'tpl': _feed_tpl})
            self.write_feed(posts, dest, **params)
