#!/usr/bin/env python

import os
import datetime
from liquidluck.writers.base import Pagination
from liquidluck.writers.base import get_post_slug
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


def test_load_jinja():
    load_jinja()
