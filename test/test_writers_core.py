#!/usr/bin/env python

import os
import datetime
from liquidluck.writers.base import get_post_slug, slug_to_destination
from liquidluck.writers.base import content_url, static_url
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


def test_content_url():
    assert content_url('index.html') == '/'

    settings.permalink = '{{category}}/{{filename}}.html'
    assert content_url(10) == '/10.html'
    assert content_url('a') == '/a.html'
    assert content_url('a.html') == '/a.html'
    assert content_url('a/') == '/a.html'
    assert content_url('a', 'b') == '/a/b.html'
    assert content_url('a/index.html') == '/a/'
    assert content_url('a/feed.xml') == '/a/feed.xml'
    assert content_url(10) == '/10.html'

    settings.permalink = '{{category}}/{{filename}}'
    assert content_url('a') == '/a'
    assert content_url('a.html') == '/a'
    assert content_url('a/') == '/a'
    assert content_url('a', 'b') == '/a/b'
    assert content_url('a/index.html') == '/a/'
    assert content_url('a/feed.xml') == '/a/feed'
    assert content_url(10) == '/10'

    settings.permalink = '{{category}}/{{filename}}/'
    assert content_url('a') == '/a/'
    assert content_url('a.html') == '/a/'
    assert content_url('a/') == '/a/'
    assert content_url('a', 'b') == '/a/b/'
    assert content_url('a/index.html') == '/a/'
    assert content_url('a/feed.xml') == '/a/feed/'
    assert content_url(10) == '/10/'


def test_static_url():
    path = os.path.join(ROOT, 'source')
    func = static_url(path)
    func('settings.py')


class TestPostWriter(object):
    def test_start(self):
        #: if test_cli.py run first
        writer = PostWriter()
        writer.start()
        settings.permalink = '{{date.year}}/{{filename}}.html'
        writer.start()


class TestPageWriter(object):
    def test_start(self):
        writer = PageWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'demo-page.html')
        assert os.path.exists(f)


class TestArchiveWriter(object):
    def test_start(self):
        writer = ArchiveWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'index.html')
        assert os.path.exists(f)


class TestArchiveFeedWriter(object):
    def test_start(self):
        writer = ArchiveFeedWriter()
        writer.start()
        f = os.path.join(g.output_directory, 'feed.xml')
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
