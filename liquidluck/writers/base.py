#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Writer, write your content to html.

:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''


import os
import re
from jinja2 import Environment, FileSystemLoader
from liquidluck.utils import import_object, to_unicode

# blog settings
from liquidluck.options import settings

# liquidluck settings
from liquidluck.options import g


class BaseWriter(object):
    """BaseWriter
    """
    def begin(self):
        pass

    def run(self):
        raise NotImplementedError

    def write(self, content, destination):
        folder = os.path.split(destination)[0]
        # on Mac OSX, `folder` == `FOLDER`
        # then make sure destination is lowercase
        if not os.path.isdir(folder):
            os.makedirs(folder)

        f = open(destination, 'w')
        f.write(content.encode('utf-8'))
        f.close()
        return

    def render(self, params, template, destination):
        tpl = g.jinja.get_template(template)
        html = tpl.render(params)
        self.write(html, destination)
        #: logging
        return

    def destination_of_post(self, post):
        slug = get_post_slug(post, settings.permalink)
        return os.path.join(settings.deploydir, slug_to_destination(slug))


class Pagination(object):
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
        return (self.total - 1) / self.per_page + 1

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
    loaders = []
    tpl = os.path.abspath('_templates')
    if os.path.exists(tpl):
        loaders.append(tpl)

    theme = os.path.join(
        os.path.abspath('_themes'), settings.theme, 'templates'
    )
    if os.path.exists(theme):
        loaders.append(theme)
    else:
        loaders.append(
            os.path.join(
                g.liquid_directory,
                '_themes',
                settings.theme,
                'templates'
            )
        )

    jinja = Environment(
        loader=FileSystemLoader(loaders),
        autoescape=False,  # blog don't need autoescape
        extensions=settings.jinja_extensions or [],
    )

    jinja.globals = settings.jinja_variables or {}

    #: TODO add default filters
    if settings.jinja_filters is None:
        settings.jinja_filters = {}

    for k, v in settings.jinja_filters.items():
        jinja.filters.update({k: import_object(v)})

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
