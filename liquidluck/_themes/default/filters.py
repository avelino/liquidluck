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


def description(key):
    from liquidluck.options import settings
    dct = settings.theme_variables.get('descriptions')
    if not isinstance(dct, dict):
        return ''
    if key not in dct:
        return ''
    return dct[key]
