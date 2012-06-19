#!/usr/bin/env python

import os
from liquidluck.writers.extends import PostWriter
from liquidluck.options import g

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestPostWriter(object):
    def test_get_relations(self):
        post = g.public_posts[0]
        writer = PostWriter()
        relation = writer._get_relations(post, 0)
        assert relation['newer'] is None
        assert relation['older'] is not None
        assert relation['related'] is not None
