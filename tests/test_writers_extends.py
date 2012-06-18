#!/usr/bin/env python

import os
from liquidluck.writers.extends import YearWriter, TagWriter
from liquidluck.writers.extends import CategoryWriter, CategoryFeedWriter
from liquidluck.writers.extends import RelationalPostWriter
from liquidluck.options import g

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestYearWriter(object):
    def test_start(self):
        writer = YearWriter()
        writer.start()
        f = os.path.join(g.output_directory, '2012/index.html')
        assert os.path.exists(f)


class TestTagWriter(object):
    def test_start(self):
        writer = TagWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'tag/tag1/index.html')
        assert os.path.exists(f)


class TestCategoryWriter(object):
    def test_start(self):
        writer = CategoryWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'work/index.html')
        assert os.path.exists(f)


class TestCategoryFeedWriter(object):
    def test_start(self):
        writer = CategoryFeedWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'work/feed.xml')
        assert os.path.exists(f)


class TestRelationalPostWriter(object):
    def test_get_relations(self):
        post = g.public_posts[0]
        writer = RelationalPostWriter()
        relation = writer._get_relations(post, 0)
        assert relation['newer'] is None
        assert relation['older'] is not None
        assert relation['related'] is not None
