#!/usr/bin/env python

import os.path
import datetime
from liquidluck.options import settings
from liquidluck.readers.base import Post
from liquidluck.readers.markdown import MarkdownReader

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestPost(object):
    def setUp(self):
        self.meta = {
            'author': 'lepture',
            'date': '2012-12-12',
            'tags': 'life, work',
        }

    def test_author(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.author == 'lepture'

    def test_embed_author(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.embed_author == 'lepture'

        settings.authors = {
            'lepture': {
                'name': 'Hsiaoming Yang',
            }
        }
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.embed_author == 'Hsiaoming Yang'

        settings.authors = {
            'lepture': {
                'email': 'lepture@me.com',
            }
        }
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.embed_author == (
            '<a href="mailto:lepture@me.com">lepture</a>')

        settings.authors = {
            'lepture': {
                'website': 'http://lepture.com',
            }
        }
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.embed_author == (
            '<a href="http://lepture.com">lepture</a>')

    def test_date(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.date == datetime.datetime(2012, 12, 12)

    def test_public(self):
        meta = {'public': 'false'}
        post = Post('filepath', 'content', title='title', meta=meta)
        assert post.public is False

        post = Post('filepath', 'content', title='title', meta={})
        assert post.public is True

        meta = {'public': 'true'}
        post = Post('filepath', 'content', title='title', meta=meta)
        assert post.public is True

    def test_tags(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.tags == ['life', 'work']


class TestMarkdownReader(object):
    def setUp(self):
        path = os.path.join(ROOT, 'source/post/demo-markdown-1.md')
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