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
import hashlib
import logging
from jinja2 import Environment, FileSystemLoader
import liquidluck
from liquidluck.utils import import_object, to_unicode, to_bytes, utf8

# blog settings
from liquidluck.options import settings

# liquidluck settings
from liquidluck.options import g
from liquidluck.filters import xmldatetime, feed_updated
from liquidluck.filters import tag_url, year_url


class BaseWriter(object):
    """BaseWriter
    """
    def start(self):
        raise NotImplementedError

    def run(self):
        if g.detail_logging:
            self.start()
        else:
            try:
                self.start()
            except Exception as e:
                logging.error(e)

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
        if g.detail_logging:
            logging.info('write %s' % filepath)
        tpl = g.jinja.get_template(template)
        html = tpl.render(params)
        self.write(html, os.path.join(g.output_directory, filepath))
        return

    def get(self, key, value=None):
        return settings.writers_variables.get(key, value)

    @property
    def perpage(self):
        return settings.perpage


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


def load_jinja():
    #: prepare loaders
    #: loaders = ['_templates', theme]
    loaders = []
    tpl = os.path.abspath('_templates')
    if os.path.exists(tpl):
        loaders.append(tpl)

    theme = os.path.join(os.path.abspath('_themes'), settings.theme)
    if not os.path.exists(theme):
        theme = os.path.join(g.liquid_directory, '_themes', settings.theme)
    if not os.path.exists(theme):
        logging.error("Can't find theme: %s" % settings.theme)

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
        extensions=settings.template_extensions or [],
    )
    #: initialize globals
    jinja.globals = {}

    #: load template variables
    jinja.globals.update({
        'site': settings.site,
        'template': settings.template_variables,
    })

    #: load theme variables
    config = {}
    theme_config = os.path.join(theme, 'settings.py')
    if os.path.exists(theme_config):
        execfile(theme_config, {}, config)

    #: user can reset theme variables
    config.update(settings.theme_variables)
    #: keep namespace to the latest variables
    settings.theme_variables = config
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
    filters = settings.template_filters or {}
    for k, v in filters.items():
        jinja.filters.update({k: import_object(v)})

    #: default filters
    jinja.filters.update({
        'xmldatetime': xmldatetime,
        'feed_updated': feed_updated,
        'permalink': permalink,
        'tag_url': tag_url,
        'year_url': year_url,
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


def slug_to_destination(slug, use_index=False):
    if slug.endswith('.html'):
        return slug

    if slug.endswith('/') and use_index:
        return slug + 'index.html'

    return slug.rstrip('/') + '.html'


def permalink(post, prepend_site=False):
    slug = get_post_slug(post, settings.permalink)
    if prepend_site:
        url = '%s/%s' % (settings.site['url'].rstrip('/'), slug)
    else:
        url = '/%s' % slug

    if url.endswith('/index.html'):
        return url[:-10]
    return url


def content_url(base, *args):
    def fix_index(url):
        if url.endswith('/index.html'):
            return url[:-10]
        return url

    args = list(args)
    base = to_unicode(base)

    if base.startswith('http://') or base.startswith('https://'):
        prefix = '%s/' % base.rstrip('/')
    else:
        prefix = '/'
        args.insert(0, base)

    args = map(lambda o: to_unicode(o).strip('/'), args)
    url = '/'.join(args).replace('//', '/').replace(' ', '-')
    url = prefix + url.lstrip('/')
    url = to_unicode(fix_index(url.lower()))

    if url.endswith('/'):
        return url

    if settings.permalink.endswith('.html'):
        if url.endswith('.html'):
            return url
        if url.endswith('.xml'):
            return url
        return '%s.html' % url

    if settings.permalink.endswith('/'):
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

    def create_url(path):
        hsh = get_hsh(path)[:5]
        url = '%s/%s?v=%s' % (settings.static_prefix.rstrip('/'), path, hsh)
        return url

    return create_url
