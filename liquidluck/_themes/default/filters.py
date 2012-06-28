#!/usr/bin/env python


def tag_url(tag):
    from liquidluck.writers.base import content_url
    from liquidluck.options import settings
    prefix = settings.site.get('prefix', '')
    return content_url(prefix, 'tag', tag, 'index.html')


def year_url(post):
    from liquidluck.writers.base import content_url
    from liquidluck.options import settings
    prefix = settings.site.get('prefix', '')
    return content_url(prefix, post.date.year, 'index.html')


def tagcloud_url(tag):
    from liquidluck.writers.base import content_url
    from liquidluck.options import settings
    prefix = settings.site.get('prefix', '')
    return '%s#%s' % (content_url(prefix, 'tag', 'index.html'), tag)
