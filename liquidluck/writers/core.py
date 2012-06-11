#!/usr/bin/env python

import logging
from liquidluck.options import g
from liquidluck.writers.base import BaseWriter


class PostWriter(BaseWriter):
    def run(self):
        for post in g.public_posts:
            self.render(
                {'post': post}, 'post.html', self.destination_of_post(post)
            )

        logging.info('PostWriter Finished')
