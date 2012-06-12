#!/usr/bin/env python

import os
from liquidluck.writers.extends import YearWriter, TagWriter
from liquidluck.options import settings

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestYearWriter(object):
    def test_run(self):
        writer = YearWriter()
        writer.run()
        f = os.path.join(os.getcwd(), settings.deploydir, '2012/index.html')
        assert os.path.exists(f)


class TestTagWriter(object):
    def test_run(self):
        writer = TagWriter()
        writer.run()
        f = os.path.join(
            os.getcwd(), settings.deploydir, 'tags/tag1/index.html'
        )
        assert os.path.exists(f)
