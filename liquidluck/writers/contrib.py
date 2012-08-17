#!/usr/bin/env python

"""Writers from contributors
"""

import os
import datetime
from liquidluck.options import g
from liquidluck.writers.base import BaseWriter, permalink
try:
    import json
    json_encode = json.dumps
except ImportError:
    import simplejson
    json_encode = simplejson.dumps


class DataJsonWriter(BaseWriter):
    """Provide a json file that contains all the meta info::

        /data.json

        {
            "updated": "2012-12-12 12:12:12",
            "posts": [],
            "pages": []
        }
    """

    def start(self):
        strftime = lambda o: o.strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.utcnow()
        container = {
            "updated": strftime(now),
            "posts": [], "pages": [],
        }

        for post in g.public_posts:
            dct = {}
            dct['title'] = post.title
            dct['date'] = strftime(post.date)
            dct['category'] = post.category
            dct['filepath'] = post.clean_filepath
            dct['url'] = permalink(post)
            container['posts'].append(dct)

        for post in g.pure_pages:
            dct = {}
            dct['title'] = post.title
            dct['date'] = strftime(post.updated)
            dct['filepath'] = post.clean_filepath
            container['pages'].append(dct)

        data = json_encode(container, ensure_ascii=False)
        output = os.path.join(g.output_directory, 'data.json')
        self.write(data, output)
