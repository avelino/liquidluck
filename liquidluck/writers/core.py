#!/usr/bin/env python

import os
import logging
from liquidluck.options import g, settings
from liquidluck.writers.base import BaseWriter, Pagination


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
            dest = os.path.join(settings.deploydir, 'page/%s.html' % page)
            self.render({'pagination': pagination}, 'archive.html', dest)

        logging.info('ArchiveWriter Finished')


class ArchiveFeedWriter(BaseWriter):
    def run(self):
        posts = g.public_posts[settings.feedcount]
        dest = os.path.join(settings.deploydir, 'feed.xml')
        self.render({'posts': posts}, 'feed.xml', dest)
