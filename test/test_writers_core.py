#!/usr/bin/env python

import os
import datetime
from liquidluck.writers.base import get_post_slug, slug_to_destination
from liquidluck.writers.base import linkmaker
from liquidluck.writers.core import PostWriter, PageWriter
from liquidluck.writers.core import ArchiveWriter, ArchiveFeedWriter
from liquidluck.writers.core import FileWriter, StaticWriter
from liquidluck.options import settings, g

ROOT = os.path.abspath(os.path.dirname(__file__))


def test_get_post_slug():
    class Post:
        filename = 'demo'

        @property
        def category(self):
            return 'life'

        @property
        def date(self):
            return datetime.datetime(2012, 12, 12)

        @property
        def folder(self):
            return None

    post = Post()

    slug_format = '{{category}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == 'life/demo.html'

    slug_format = '{{date.year}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == '2012/demo.html'

    slug_format = '{{folder}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == 'demo.html'


def test_slug_to_destination():
    assert slug_to_destination('a/b.html') == 'a/b.html'
    assert slug_to_destination('a/b/') == 'a/b.html'
    assert slug_to_destination('a/b/', True) == 'a/b/index.html'
    assert slug_to_destination('a/b') == 'a/b.html'


def test_linkmarker():
    url = 'http://lepture.com'
    settings.site['url'] = url
    assert linkmaker('index.html') == (url + '/')

    settings.linktype = 'html'
    assert linkmaker('a') == '%s/a.html' % url
    assert linkmaker('a.html') == '%s/a.html' % url
    assert linkmaker('a/') == '%s/a.html' % url
    assert linkmaker('a', 'b') == '%s/a/b.html' % url
    assert linkmaker('a/index.html') == '%s/a/' % url
    assert linkmaker('a/feed.xml') == '%s/a/feed.xml' % url

    settings.linktype = 'clean'
    assert linkmaker('a') == '%s/a' % url
    assert linkmaker('a.html') == '%s/a' % url
    assert linkmaker('a/') == '%s/a' % url
    assert linkmaker('a', 'b') == '%s/a/b' % url
    assert linkmaker('a/index.html') == '%s/a/' % url
    assert linkmaker('a/feed.xml') == '%s/a/feed' % url

    settings.linktype = 'slash'
    assert linkmaker('a') == '%s/a/' % url
    assert linkmaker('a.html') == '%s/a/' % url
    assert linkmaker('a/') == '%s/a/' % url
    assert linkmaker('a', 'b') == '%s/a/b/' % url
    assert linkmaker('a/index.html') == '%s/a/' % url
    assert linkmaker('a/feed.xml') == '%s/a/feed/' % url


class TestPostWriter(object):
    def test_run(self):
        #: if test_cli.py run first
        writer = PostWriter()
        writer.run()
        settings.permalink = '{{date.year}}/{{filename}}.html'
        writer.run()


class TestPageWriter(object):
    def test_run(self):
        writer = PageWriter()
        writer.run()
        f = os.path.join(g.output_directory, 'demo-page.html')
        assert os.path.exists(f)


class TestArchiveWriter(object):
    def test_run(self):
        writer = ArchiveWriter()
        writer.run()
        f = os.path.join(g.output_directory, 'index.html')
        assert os.path.exists(f)


class TestArchiveFeedWriter(object):
    def test_run(self):
        writer = ArchiveFeedWriter()
        writer.run()
        f = os.path.join(g.output_directory, 'feed.xml')
        assert os.path.exists(f)


class TestFileWriter(object):
    def test_run(self):
        writer = FileWriter()
        writer.run()
        f = os.path.join(g.output_directory, 'media/hold.txt')
        assert os.path.exists(f)


class TestStaticWriter(object):
    def test_run(self):
        writer = StaticWriter()
        writer.run()
        f = os.path.join(g.static_directory, 'style.css')
        assert os.path.exists(f)
