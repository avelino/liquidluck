#!/usr/bin/env python

"""Writers from contributors
"""

import os
import json
import logging
from liquidluck.options import g, settings
from liquidluck.filters import xmldatetime
from liquidluck.writers.core import ArchiveWriter
from liquidluck.writers.base import get_post_destination


class TagJSONWriter(ArchiveWriter):
    writer_name = 'json'

    def __init__(self):
        self._tags_dict = {}
        self._output = self.get('json', self.prefix_dest('tags.json'))
        for post in g.public_posts:
            for tag in post.tags:
                tag = tag.lower()
                if tag not in self._tags_dict:
                    self._tags_dict[tag] = []
                self._tags_dict[tag].append({
                    'title': post.title,
                    'url': '/' + get_post_destination(post,
                    settings.config['permalink']),
                    'datetime': xmldatetime(post.date)
                })

    def start(self):
        dest = os.path.join(g.output_directory, self._output)
        with open(dest, 'w') as json_file:
            json.dump(self._tags_dict, json_file)
        logging.debug('write %s' % self._output)
