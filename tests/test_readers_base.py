# coding: utf-8

import datetime
from liquidluck.readers._base import Post


class TestPost(object):
    def test_without_source(self):
        post = Post('', 'foo', 'foobar', {})
        assert post.title == ''
        assert post.relative_filepath == 'foo'
        assert post.clean_title == ''
        assert post.date is None
        assert post.public
        assert post.template is None
        assert post.category is None
        assert len(post.tags) == 0

    def test_with_source(self):
        post = Post('foo', 'foo/bar', 'foobar', {})
        assert post.relative_filepath == 'bar'

    def test_clean_title(self):
        post = Post('foo', 'foo/bar', 'foobar', {
            'title': 'foo bar'
        })
        assert post.clean_title == 'foo-bar'

        post = Post('foo', 'foo/bar', 'foobar', {
            'title': '#foo <bar>'
        })
        assert post.clean_title == 'foo-bar'

    def test_date(self):
        post = Post('foo', 'foo/bar', 'foobar', {
            'date': '2013-08-07'
        })
        assert post.date == datetime.datetime(2013, 8, 7)

        post = Post('foo', 'foo/bar', 'foobar', {
            'date': '20130807'
        })
        assert post.date == datetime.datetime(2013, 8, 7)

    def test_tags(self):
        post = Post('foo', 'foo/bar', 'foobar', {
            'tags': ['python', 'javascript']
        })
        assert post.tags == ['python', 'javascript']

        post = Post('foo', 'foo/bar', 'foobar', {
            'tags': 'python, javascript'
        })
        assert post.tags == ['python', 'javascript']

    def test_public(self):
        post = Post('foo', 'foo/bar', 'foobar', {
            'status': 'public'
        })
        assert post.public

        post = Post('foo', 'foo/bar', 'foobar', {
            'status': 'draft'
        })
        assert not post.public

        post = Post('foo', 'foo/bar', 'foobar', {
            'public': 'false'
        })
        assert not post.public

        post = Post('foo', 'foo/bar', 'foobar', {
            'public': 'true'
        })
        assert post.public
