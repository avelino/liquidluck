#!/usr/bin/env python

import os
import datetime
from liquidluck.writers.base import get_post_slug, slug_to_destination
from liquidluck.writers.core import PostWriter, ArchiveWriter
from liquidluck.writers.core import ArchiveFeedWriter, FileWriter
from liquidluck.options import settings

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


class TestPostWriter(object):
    def test_run(self):
        #: if test_cli.py run first
        writer = PostWriter()
        writer.run()
        settings.permalink = '{{date.year}}/{{filename}}.html'
        writer.run()


class TestArchiveWriter(object):
    def test_run(self):
        writer = ArchiveWriter()
        writer.run()


class TestArchiveFeedWriter(object):
    def test_run(self):
        writer = ArchiveFeedWriter()
        writer.run()
        f = os.path.join(os.getcwd(), settings.deploydir, 'feed.xml')
        assert os.path.exists(f)


class TestFileWriter(object):
    def test_run(self):
        writer = FileWriter()
        writer.run()
        #: travis-ci bug
        #f = os.path.join(os.getcwd(), settings.deploydir, 'media/hold.txt')
        #assert os.path.exists(f)
