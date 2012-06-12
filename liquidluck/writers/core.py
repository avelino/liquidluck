#!/usr/bin/env python

import os
import logging
import shutil
from liquidluck.options import g, settings
from liquidluck.utils import UnicodeDict, walk_dir
from liquidluck.writers.base import BaseWriter, Pagination, linkmaker
from liquidluck.writers.base import get_post_slug, slug_to_destination


class PostWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('post_template', 'post.html')

    def run(self):
        for post in g.public_posts:
            self.render(
                {'post': post}, 'post.html', self._dest_of(post)
            )

        for post in g.secure_posts:
            self.render(
                {'post': post}, 'post.html', self._dest_of(post)
            )

        logging.info('PostWriter Finished')

    def _dest_of(self, post):
        slug = get_post_slug(post, settings.permalink)
        return os.path.join(g.output_directory, slug_to_destination(slug))


class ArchiveWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('archive_template', 'archive.html')
        self._output = self.get('archive_output', 'index.html')

    def run(self):
        self._write_posts()
        logging.info('ArchiveWriter Finished')

    def _write_posts(self):
        pagination = Pagination(g.public_posts, 1, self.perpage)
        pagination.title = 'Archive'

        dest = os.path.join(g.output_directory, self._output)
        self.render({'pagination': pagination}, self._template, dest)

        if pagination.pages < 2:
            return

        for page in range(1, pagination.pages + 1):
            pagination = Pagination(g.public_posts, page, self.perpage)
            dest = os.path.join(g.output_directory, 'page/%s.html' % page)
            self.render({'pagination': pagination}, self._template, dest)


class ArchiveFeedWriter(BaseWriter):
    def __init__(self):
        self._template = self.get('archive_feed_template', 'feed.xml')

        self.feed = UnicodeDict()
        self.feed.url = settings.site['url']

        self._output = self.get('archive_feed_output', 'feed.xml')
        self.feed.feedurl = linkmaker(self._output)

    def run(self):
        self.feed.posts = g.public_posts[:settings.feedcount]
        dest = os.path.join(g.output_directory, self._output)
        print g.output_directory
        self.render({'feed': self.feed}, self._template, dest)


class FileWriter(BaseWriter):
    def run(self):
        l = len(g.source_directory) + 1
        for f in g.pure_files:
            path = f[l:]
            dest = os.path.join(g.output_directory, path)
            copy_to(f, dest)

        logging.info('FileWriter Finished')


class StaticWriter(BaseWriter):
    def run(self):
        static_path = os.path.join(g.theme_directory, 'static')
        l = len(static_path) + 1
        for f in walk_dir(static_path):
            path = f[l:]
            dest = os.path.join(g.static_directory, path)
            copy_to(f, dest)

        logging.info('StaticWriter Finished')


def copy_to(source, dest):
    if os.path.exists(dest) and \
       os.stat(source).st_mtime <= os.stat(dest).st_mtime:
        return

    folder = os.path.split(dest)[0]
    # on Mac OSX, `folder` == `FOLDER`
    # then make sure destination is lowercase
    if not os.path.isdir(folder):
        os.makedirs(folder)

    shutil.copy(source, dest)
    return
