#!/usr/bin/env python

import os
import datetime
from liquidluck.writers.base import Pagination
from liquidluck.writers.base import get_post_slug, slug_to_destination
from liquidluck.writers.base import content_url, static_url
from liquidluck.writers.base import load_jinja
from liquidluck.options import settings

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestPagination(object):
    def test_pages(self):
        p = Pagination(range(6), 1, 3)
        assert p.pages == 2

        p = Pagination(range(5), 1, 3)
        assert p.pages == 2

        p = Pagination(range(7), 1, 3)
        assert p.pages == 3

    def test_items(self):
        items = [0, 1, 2, 3, 4, 5]
        p = Pagination(items, 1, 3)
        assert p.items == [0, 1, 2]

        p = Pagination(items, 2, 3)
        assert p.items == [3, 4, 5]


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

    settings.site['prefix'] = ''
    slug_format = '{{category}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == 'life/demo.html'

    slug_format = '{{date.year}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == '2012/demo.html'

    slug_format = '{{folder}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == 'demo.html'

    settings.site['prefix'] = 'blog'
    slug_format = '{{category}}/{{filename}}.html'
    assert get_post_slug(post, slug_format) == 'blog/life/demo.html'


def test_slug_to_destination():
    settings.site['prefix'] = ''
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
    path = os.path.join(ROOT, 'source', 'post')
    func = static_url(path)
    func('demo-rst-1.rst')


def test_load_jinja():
    load_jinja()
