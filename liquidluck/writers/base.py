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
from jinja2 import Environment, FileSystemLoader
from liquidluck.utils import import_object, to_unicode, utf8

# blog settings
from liquidluck.options import settings

# liquidluck settings
from liquidluck.options import g


class BaseWriter(object):
    """BaseWriter
    """
    def run(self):
        raise NotImplementedError

    def write(self, content, destination):
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
        tpl = g.jinja.get_template(template)
        html = tpl.render(params)
        self.write(html, destination)
        #: logging
        return

    def get(self, key, value=None):
        return settings.writers_variables.get(key, value)

    @property
    def perpage(self):
        return settings.perpage


class Pagination(object):
    title = None
    url = None

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
        return len(self.items)

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

    #: global variable
    g.theme_directory = theme

    theme_template = os.path.join(theme, 'templates')
    if os.path.exists(theme_template):
        loaders.append(theme_template)

    #: init jinja
    jinja = Environment(
        loader=FileSystemLoader(loaders),
        autoescape=False,  # blog don't need autoescape
        extensions=settings.template_extensions or [],
    )

    #: load theme config
    config = {}
    theme_config = os.path.join(theme, 'config.py')
    if os.path.exists(theme_config):
        execfile(theme_config, {}, config)

    filters = config.pop('filters', {})
    jinja.globals = config
    jinja.filters.update(filters)

    # load variables from settings
    jinja.globals.update(settings.template_variables or {})

    #: default variables
    jinja.globals.update({
        'site': settings.site,
        'now': datetime.datetime.now(),
        'linkmaker': linkmaker,
    })

    #: load filters from settings
    filters = settings.template_filters or {}
    for k, v in filters.items():
        jinja.filters.update({k: import_object(v)})

    #: default filters
    jinja.filters.update({
        'xmldatetime': lambda o: o.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'postlink': postlink,
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
        return to_unicode(value)

    slug = regex.sub(replace, slug_format)
    slug = slug.lstrip('/').replace('//', '/')
    return slug


def slug_to_destination(slug, use_index=False):
    if slug.endswith('.html'):
        return slug

    if slug.endswith('/') and use_index:
        return slug + 'index.html'

    return slug.rstrip('/') + '.html'


def postlink(post):
    slug = get_post_slug(post, settings.permalink)
    siteurl = settings.site['url'].rstrip('/')
    return '%s/%s' % (siteurl, slug)


def linkmaker(base, *args):
    siteurl = settings.site['url'].rstrip('/')
    args = list(args)
    args.insert(0, base)
    args = map(lambda o: str(o).strip('/'), args)
    url = '%s/%s' % (siteurl, '/'.join(args))
    if settings.linktype == 'html':
        if url.endswith('.html'):
            return url
        if url.endswith('.xml'):
            return url
        return '%s.html' % url

    if settings.linktype == 'clean':
        if url.endswith('.html'):
            return url.rstrip('.html')
        if url.endswith('.xml'):
            return url.rstrip('.xml')
        return url

    if settings.linktype == 'slash':
        if url.endswith('.html'):
            url = url.rstrip('.html')
        if url.endswith('.xml'):
            url = url.rstrip('.xml')

        return '%s/' % url
