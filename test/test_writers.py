#!/usr/bin/env python

import datetime
from liquidluck.writers.base import get_post_slug, slug_to_destination


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
