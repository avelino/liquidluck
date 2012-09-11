#!/usr/bin/env python

import os
from liquidluck.writers.core import PostWriter, PageWriter
from liquidluck.writers.core import ArchiveWriter, ArchiveFeedWriter
from liquidluck.writers.core import FileWriter, StaticWriter
from liquidluck.writers.core import YearWriter, TagWriter
from liquidluck.writers.core import CategoryWriter, CategoryFeedWriter
from liquidluck.options import settings, g

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestPostWriter(object):
    def test_start(self):
        writer = PostWriter()
        settings.config['permalink'] = '{{category}}/{{filename}}.html'
        settings.site['prefix'] = ''
        writer.start()
        f = os.path.join(g.output_directory, 'work/demo-markdown-1.html')
        assert os.path.exists(f)

        settings.config['permalink'] = '{{date.year}}/{{filename}}.html'
        writer.start()
        f = os.path.join(g.output_directory, '2012/demo-markdown-1.html')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer.start()
        f = os.path.join(g.output_directory, 'blog/2012/demo-markdown-1.html')
        assert os.path.exists(f)


class TestPageWriter(object):
    def test_start(self):
        writer = PageWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'demo-page.html')
        assert os.path.exists(f)


class TestArchiveWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = ArchiveWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'index.html')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = ArchiveWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/index.html')
        assert os.path.exists(f)


class TestArchiveFeedWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = ArchiveFeedWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'feed.xml')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = ArchiveFeedWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/feed.xml')
        assert os.path.exists(f)


class TestFileWriter(object):
    def test_start(self):
        writer = FileWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'media/hold.txt')
        assert os.path.exists(f)


class TestStaticWriter(object):
    def test_start(self):
        writer = StaticWriter()
        writer.start()
        f = os.path.join(g.static_directory, 'style.css')
        assert os.path.exists(f)


class TestYearWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = YearWriter()
        writer.start()
        f = os.path.join(g.output_directory, '2012/index.html')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = YearWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/2012/index.html')
        assert os.path.exists(f)


class TestTagWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = TagWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'tag/tag1/index.html')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = TagWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/tag/tag1/index.html')
        assert os.path.exists(f)


class TestCategoryWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = CategoryWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'work/index.html')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = CategoryWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/work/index.html')
        assert os.path.exists(f)


class TestCategoryFeedWriter(object):
    def test_start(self):
        settings.site['prefix'] = ''
        writer = CategoryFeedWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'work/feed.xml')
        assert os.path.exists(f)

        settings.site['prefix'] = 'blog'
        writer = CategoryFeedWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'blog/work/feed.xml')
        assert os.path.exists(f)
