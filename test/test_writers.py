#!/usr/bin/env python

from liquidluck.writers.base import get_post_slug


def test_get_post_slug():
    class Post:
        filename = 'demo'

        @property
        def category(self):
            return 'life'

    post = Post()
    slug_format = '{{category}}/{{filename}}.html'

    assert get_post_slug(post, slug_format) == 'life/demo.html'
