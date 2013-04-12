#!/usr/bin/env python

import os
from liquidluck.writers.contrib import TagJSONWriter
from liquidluck.options import settings, g

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestTagJSONWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = TagJSONWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'tags.json')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = TagJSONWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/tags.json')
        assert os.path.exists(f)
