#!/usr/bin/env python

import os.path
from liquidluck.readers.markdown import MarkdownReader

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestMarkdownReader(object):
    def setUp(self):
        path = os.path.join(ROOT, 'source/post/demo.md')
        self.reader = MarkdownReader(path)
        self.post = self.reader.render()

    def test_title(self):
        assert self.post.title == 'demo'

    def test_tags(self):
        assert self.post.tags == ['tag1', 'tag2']

    def test_public(self):
        assert self.post.public is True

    def test_pygments(self):
        assert 'highlight' in self.post.content
