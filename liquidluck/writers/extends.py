#!/usr/bin/env python

import os
import logging
from liquidluck.options import g, settings
from liquidluck.writers.base import BaseWriter, Pagination


class YearWriter(BaseWriter):
    _year_posts = {}

    def _split_posts(self):
        for post in g.public_posts:
            if post.date.year not in self._year_posts:
                self._year_posts[post.date.year] = [post]
            else:
                self._year_posts[post.date.year].append(post)

    def run(self):
        self._split_posts()

        for year in self._year_posts:
            posts = self._year_posts[year]
            #: TODO need pagination for year ?
            pagination = Pagination(posts, 1, settings.perpage)
            pagination.title = year

            dest = os.path.join(settings.deploydir, str(year), 'index.html')
            self.render({'pagination': pagination}, 'archive.html', dest)

            for page in range(1, pagination.pages + 1):
                dest = os.path.join(
                    settings.deploydir, str(year), 'page/%s.html' % page)
                pagination = Pagination(posts, page, settings.perpage)
                pagination.title = year
                self.render({'pagination': pagination}, 'archive.html', dest)

        logging.info('YearWriter Finished')


class TagWriter(BaseWriter):
    _tag_posts = {}

    def _split_posts(self):
        for post in g.public_posts:
            for tag in post.tags:
                if tag not in self._tag_posts:
                    self._tag_posts[tag] = [post]
                else:
                    self._tag_posts[tag].append(post)

    def run(self):
        self._split_posts()

        for tag in self._tag_posts:
            posts = self._tag_posts[tag]
            pagination = Pagination(posts, 1, settings.perpage)
            pagination.title = tag

            dest = os.path.join(settings.deploydir, 'tags', tag, 'index.html')
            self.render({'pagination': pagination}, 'archive.html', dest)

            for page in range(1, pagination.pages + 1):
                dest = os.path.join(
                    settings.deploydir, 'tags', tag, 'page/%s.html' % page)
                pagination = Pagination(posts, page, settings.perpage)
                pagination.title = tag
                self.render({'pagination': pagination}, 'archive.html', dest)

        logging.info('TagWriter Finished')
