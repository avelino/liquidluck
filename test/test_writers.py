#!/usr/bin/env python

from liquidluck.writers.base import parse_post_destination


def test_parse_post_destination():
    class Post:
        filename = 'demo'

        @property
        def category(self):
            return 'life'

    post = Post()
    slug_format = '{{category}}/{{filename}}.html'

    assert parse_post_destination(post, slug_format) == 'life/demo.html'
