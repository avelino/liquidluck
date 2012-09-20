#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Writer, write your content to html.

:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''


import os
import re
import datetime
import logging
from jinja2 import Environment, FileSystemLoader
from jinja2 import contextfilter
import liquidluck
from liquidluck.utils import import_object, get_relative_base
from liquidluck.utils import to_unicode, utf8

# blog settings
from liquidluck.options import settings

# liquidluck settings
from liquidluck.options import g
from liquidluck.filters import xmldatetime, feed_updated, wiki_link
from liquidluck.filters import content_url, tag_url, year_url, static_url


class BaseWriter(object):
    """BaseWriter
    """
    writer_name = 'base'

    def start(self):
        raise NotImplementedError

    def run(self):
        try:
            self.start()
        except Exception as e:
            logging.error(e)
            if g.interrupt:
                raise e

        name = self.__class__.__name__
        logging.info('%s Finished' % name)

    def write(self, content, destination):
        destination = destination.replace(' ', '-')
        folder = os.path.split(destination)[0]
        # on Mac OSX, `folder` == `FOLDER`
        # then make sure destination is lowercase
        if not os.path.isdir(folder):
            os.makedirs(folder)

        f = open(destination, 'w')
        f.write(utf8(content))
        f.close()
        return

    def render(self, params, template, destination):
        filepath = destination[len(g.output_directory) + 1:]
        filepath = filepath.lower()
        logging.debug('write %s' % filepath)
        tpl = g.jinja.get_template(template)

        writer = {
            'class': self.__class__.__name__,
            'name': self.writer_name,
            'filepath': filepath,
        }
        params['writer'] = writer
        html = tpl.render(params)
        self.write(html, os.path.join(g.output_directory, filepath))
        return

    def get(self, key, value=None):
        variables = settings.writer.get('vars')
        if isinstance(variables, dict):
            return variables.get(key, value)
        return value

    @property
    def perpage(self):
        return settings.config['perpage']


class Pagination(object):
    title = None
    root = ''

    def __init__(self, items, page, per_page):
        self.total_items = items
        self.page = page
        self.per_page = per_page

    def iter_pages(self, edge=4):
        if self.page <= edge:
            return range(1, min(self.pages, 2 * edge + 1) + 1)
        if self.page + edge > self.pages:
            return range(max(self.pages - 2 * edge, 1), self.pages + 1)
        return range(self.page - edge, min(self.pages, self.page + edge) + 1)

    @property
    def pages(self):
        return int((self.total - 1) / self.per_page) + 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.page + 1

    @property
    def total(self):
        return len(self.total_items)

    @property
    def items(self):
        start = (self.page - 1) * self.per_page
        end = self.page * self.per_page
        return self.total_items[start:end]


def find_theme():
    theme_name = settings.theme.get('name', 'default')
    theme_gallery = [
        os.path.join(os.path.abspath('_themes'), theme_name),
        os.path.join(g.theme_gallery, theme_name),
        os.path.join(g.liquid_directory, '_themes', theme_name),
    ]
    for path in theme_gallery:
        if os.path.exists(path):
            return path

    raise Exception("Can't find theme: %s" % theme_name)


def load_jinja():
    #: prepare loaders
    #: loaders = ['_templates', theme]
    loaders = []
    tpl = os.path.abspath('_templates')
    if os.path.exists(tpl):
        loaders.append(tpl)

    theme = find_theme()

    #: global variable
    g.theme_directory = theme

    theme_template = os.path.join(theme, 'templates')
    if os.path.exists(theme_template):
        loaders.append(theme_template)

    #: load default theme template always
    default_template = os.path.join(
        g.liquid_directory, '_themes/default/templates'
    )
    if default_template != theme_template:
        loaders.append(default_template)

    #: init jinja
    jinja = Environment(
        loader=FileSystemLoader(loaders),
        autoescape=False,  # blog don't need autoescape
        extensions=settings.writer.get('extensions') or [],
    )
    #: initialize globals
    jinja.globals = {}

    #: load template variables
    jinja.globals.update({
        'site': settings.site,
        'template': settings.template.get("vars") or {},
    })

    #: load theme variables
    config = {}
    theme_config = os.path.join(theme, 'settings.py')
    if os.path.exists(theme_config):
        logging.warn('settings.py in theme is deprecated since 3.4')
        logging.warn('the name should be changed to theme.py')
        execfile(theme_config, {}, config)
    theme_config = os.path.join(theme, 'theme.py')
    if os.path.exists(theme_config):
        execfile(theme_config, {}, config)

    #: user can reset theme variables
    config.update(settings.theme.get('vars') or {})
    #: keep namespace to the latest variables
    settings.theme['vars'] = config
    jinja.globals.update({'theme': config})

    #: default variables
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    jinja.globals.update({
        'system': {
            'name': 'Felix Felicis',
            'version': liquidluck.__version__,
            'homepage': liquidluck.__homepage__,
            'time': now,
        }
    })

    #: function helpers
    jinja.globals.update({
        'content_url': content_url,
        'static_url': static_url(os.path.join(theme, 'static')),
    })

    #: load theme filters
    config = {}
    theme_config = os.path.join(theme, 'filters.py')
    if os.path.exists(theme_config):
        execfile(theme_config, {}, config)

    jinja.filters.update(config)

    #: load filters from settings
    filters = settings.template.get("filters") or {}
    for k, v in filters.items():
        jinja.filters.update({k: import_object(v)})

    #: default filters
    jinja.filters.update({
        'xmldatetime': xmldatetime,
        'feed_updated': feed_updated,
        'permalink': permalink,
        'tag_url': tag_url,
        'year_url': year_url,
        'wiki_link': wiki_link,
    })

    #: load resource
    g.resource['posts'] = g.public_posts
    g.resource['pages'] = g.pure_pages
    jinja.globals.update({
        'resource': g.resource,
    })

    g.jinja = jinja
    return jinja


def get_post_slug(post, slug_format):
    regex = re.compile(r'\{\{(.*?)\}\}')

    def replace(m):
        key = m.group(1)
        bits = key.split('.')
        value = post

        for bit in bits:
            if not hasattr(value, bit):
                return ''
            value = getattr(value, bit)

        if not value:
            return ''

        if isinstance(value, int) and value < 10:
            #: fix on month and date value
            value = '0%d' % value
        return to_unicode(value)

    slug = regex.sub(replace, slug_format)
    slug = slug.lstrip('/').replace('//', '/').replace(' ', '-')
    prefix = settings.site.get('prefix', '').rstrip('/')
    slug = slug.lower()
    if prefix:
        return '%s/%s' % (prefix, slug)
    return slug


def get_post_destination(post, slug_format):
    slug = get_post_slug(post, slug_format)
    if slug.endswith('.html'):
        return slug

    return slug.rstrip('/') + '.html'


@contextfilter
def permalink(ctx, post, prepend_site=False):
    writer = ctx.get('writer')
    slug = get_post_slug(post, settings.config["permalink"])

    if prepend_site:
        url = '%s/%s' % (settings.site['url'].rstrip('/'), slug)
    elif settings.config['relative_url'] and writer:
        base = get_relative_base(writer['filepath'])
        url = '%s/%s' % (base, slug)
    else:
        url = '/%s' % slug

    if url.endswith('/index.html'):
        return url[:-10]
    return url
