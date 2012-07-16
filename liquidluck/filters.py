#!/usr/bin/env python
# -*- coding: utf-8 -*-


def xmldatetime(value):
    """ this is a jinja filter """
    import datetime
    if not isinstance(value, datetime.datetime):
        return value
    from liquidluck.options import settings
    value = value.strftime('%Y-%m-%dT%H:%M:%S')
    return '%s%s' % (value, settings.timezone)


def feed_updated(feed):
    latest = None
    for post in feed.posts:
        if not latest:
            latest = post.updated
        elif post.updated > latest:
            latest = post.updated

    return xmldatetime(latest)


def tag_url(tag, prepend_site=False):
    from liquidluck.writers.base import content_url
    from liquidluck.options import settings
    prefix = settings.site.get('prefix', '')
    url = settings.site.get('url')
    tagcloud = settings.writers.get('tagcloud', None)
    if prepend_site and tagcloud:
        return '%s#%s' % (content_url(url, prefix, 'tag', 'index.html'), tag)
    if tagcloud:
        return '%s#%s' % (content_url(prefix, 'tag', 'index.html'), tag)
    if prepend_site:
        return content_url(url, prefix, 'tag', tag, 'index.html')
    return content_url(prefix, 'tag', tag, 'index.html')


def year_url(post):
    from liquidluck.writers.base import content_url
    from liquidluck.options import settings
    prefix = settings.site.get('prefix', '')
    return content_url(prefix, post.date.year, 'index.html')
