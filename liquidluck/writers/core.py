#!/usr/bin/env python

import os
import logging
import shutil
from liquidluck.options import g, settings
from liquidluck.utils import UnicodeDict
from liquidluck.writers.base import BaseWriter, Pagination, linkmaker


class PostWriter(BaseWriter):
    def run(self):
        for post in g.public_posts:
            self.render(
                {'post': post}, 'post.html', self.destination_of_post(post)
            )

        for post in g.secure_posts:
            self.render(
                {'post': post}, 'post.html', self.destination_of_post(post)
            )

        logging.info('PostWriter Finished')


class ArchiveWriter(BaseWriter):
    def run(self):
        pagination = Pagination(g.public_posts, 1, settings.perpage)
        dest = os.path.join(settings.deploydir, settings.archive)
        self.render({'pagination': pagination}, 'archive.html', dest)

        for page in range(1, pagination.pages + 1):
            pagination = Pagination(g.public_posts, page, settings.perpage)
            dest = os.path.join(settings.deploydir, 'page/%s.html' % page)
            self.render({'pagination': pagination}, 'archive.html', dest)

        logging.info('ArchiveWriter Finished')


class ArchiveFeedWriter(BaseWriter):
    def run(self):
        feed = UnicodeDict()
        feed.posts = g.public_posts[:settings.feedcount]
        feed.feedurl = linkmaker('feed.xml')
        feed.url = g.siteurl
        dest = os.path.join(settings.deploydir, 'feed.xml')
        self.render({'feed': feed}, 'feed.xml', dest)


class FileWriter(BaseWriter):
    def run(self):
        for f in g.pure_files:
            path = f.lstrip(g.source_directory)
            dest = os.path.join(settings.deploydir, path)
            copy_to(f, dest)

        logging.info('FileWriter Finished')


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
