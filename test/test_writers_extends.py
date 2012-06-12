#!/usr/bin/env python

import os
from liquidluck.writers.extends import YearWriter, TagWriter, CategoryWriter
from liquidluck.options import g

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestYearWriter(object):
    def test_run(self):
        writer = YearWriter()
        writer.run()
        f = os.path.join(g.output_directory, '2012/index.html')
        assert os.path.exists(f)


class TestTagWriter(object):
    def test_run(self):
        writer = TagWriter()
        writer.run()
        f = os.path.join(g.output_directory, 'tags/tag1/index.html')
        assert os.path.exists(f)


class TestCategoryWriter(object):
    def test_run(self):
        writer = CategoryWriter()
        writer.run()
        f = os.path.join(g.output_directory, 'work/index.html')
        assert os.path.exists(f)
