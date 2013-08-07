# coding: utf-8

from liquidluck.cache import Cache
import tempfile


def test_memcache():
    cache = Cache()
    assert cache.get('foo') is None

    cache.set('foo', 'foo')
    assert cache.has('foo')

    assert cache.get('foo') == 'foo'

    cache.set('bar', 'bar')
    cache.set('baz', 'baz')

    assert cache.has('bar')
    cache.clear('bar')
    assert not cache.has('bar')

    cache.flush()
    assert not cache.has('baz')
    assert not cache.has('foo')


def test_filecache():
    cachedir = tempfile.mkdtemp()
    cache = Cache(cachedir)
    assert cache.get('foo') is None

    cache.set('foo', 'foo')
    assert cache.has('foo')

    assert cache.get('foo') == 'foo'

    cache.set('bar', 'bar')
    cache.set('baz', 'baz')

    assert cache.has('bar')
    cache.clear('bar')
    assert not cache.has('bar')

    cache.flush()
    assert not cache.has('baz')
    assert not cache.has('foo')
