#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import hashlib
import logging
import datetime
from jinja2 import contextfunction, contextfilter
from liquidluck.options import g, settings
from liquidluck.utils import to_unicode, to_bytes, get_relative_base


def xmldatetime(value):
    """ this is a jinja filter """
    if not isinstance(value, datetime.datetime):
        return value
    value = value.strftime('%Y-%m-%dT%H:%M:%S')
    return '%s%s' % (value, settings.config['timezone'])


def feed_updated(feed):
    latest = None
    for post in feed.posts:
        if not latest:
            latest = post.updated
        elif post.updated > latest:
            latest = post.updated

    return xmldatetime(latest)


@contextfunction
def content_url(ctx, base, *args):
    writer = ctx.get('writer')

    def fix_index(url):
        if url.endswith('/index.html'):
            return url[:-10]
        return url

    args = list(args)
    base = to_unicode(base)
    use_relative_url = settings.config.get('relative_url', False)
    if base.startswith('http://') or base.startswith('https://'):
        prefix = '%s/' % base.rstrip('/')

    elif use_relative_url and writer:
        prefix = '%s/' % get_relative_base(writer['filepath'])
        args.insert(0, base)
    else:
        prefix = '/'
        args.insert(0, base)

    args = map(lambda o: to_unicode(o).strip('/'), args)
    url = '/'.join(args).replace('//', '/').replace(' ', '-')
    url = prefix + url.lstrip('/')
    url = to_unicode(fix_index(url.lower()))

    if url.endswith('/'):
        return url

    permalink = settings.config['permalink']
    if permalink.endswith('.html'):
        if url.endswith('.html'):
            return url
        if url.endswith('.xml'):
            return url
        return '%s.html' % url

    if permalink.endswith('/'):
        if url.endswith('.html'):
            url = fix_index(url)
            url = url.rstrip('.html')
        if url.endswith('.xml'):
            url = url.rstrip('.xml')

        return '%s/' % url

    if url.endswith('.html'):
        url = fix_index(url)
        return url.rstrip('.html')
    if url.endswith('.xml'):
        return url.rstrip('.xml')
    return url


@contextfilter
def tag_url(ctx, tag, prepend_site=False):
    prefix = settings.site.get('prefix', '')
    url = settings.site.get('url')
    writers = settings.writer['active']
    tagcloud = any((True for o in writers if 'TagCloud' in o))

    if prepend_site and tagcloud:
        return '%s#%s' % (content_url(ctx, url, prefix, 'tag', 'index.html'),
                          tag)
    if tagcloud:
        return '%s#%s' % (content_url(ctx, prefix, 'tag', 'index.html'), tag)

    if prepend_site:
        return content_url(ctx, url, prefix, 'tag', tag, 'index.html')

    return content_url(ctx, prefix, 'tag', tag, 'index.html')


@contextfilter
def year_url(ctx, post):
    prefix = settings.site.get('prefix', '')
    return content_url(ctx, prefix, post.date.year, 'index.html')


_Post = {}


@contextfilter
def wiki_link(ctx, content):
    global _Post
    from liquidluck.writers.base import permalink

    def link_post(m):
        if not _Post:
            for item in g.public_posts:
                _Post[item.title] = item

        text = m.group(1)
        if '|' in text:
            title, content = text.split('|')
        else:
            title = content = text
        if title in _Post:
            item = _Post[title]
            link = permalink(ctx, item)
            return '<a href="%s">%s</a>' % (link, content)
        return '<span class="no-reference">%s</span>' % text

    pattern = re.compile(r'\[\[([^\]]+)\]\]', re.M)
    content = pattern.sub(link_post, content)
    return content


_Cache = {}


def static_url(base):
    global _Cache

    def get_hsh(path):
        if path in _Cache:
            return _Cache[path]
        abspath = os.path.join(base, path)
        if not os.path.exists(abspath):
            logging.warn('%s does not exists' % path)
            return ''

        with open(abspath) as f:
            content = f.read()
            hsh = hashlib.md5(to_bytes(content)).hexdigest()
            _Cache[path] = hsh
            return hsh

    @contextfunction
    def create_url(ctx, path):
        hsh = get_hsh(path)[:5]
        prefix = settings.config.get('static_prefix', '/static/').rstrip('/')
        use_relative_url = settings.config.get('relative_url', False)

        if use_relative_url and not prefix.startswith('http'):
            base = get_relative_base(ctx.get('writer')['filepath'])
            prefix = '%s/%s' % (base, prefix.lstrip('/'))

        url = '%s/%s?v=%s' % (prefix, path, hsh)
        return url

    return create_url
