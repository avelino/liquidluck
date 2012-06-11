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
    @property
    def jinja(self):
        if hasattr(self, '_jinja'):
            return self._jinja

        loaders = []
        tpl = os.path.abspath('_templates')
        if os.path.exists(tpl):
            loaders.append(tpl)

        theme = os.path.join(os.path.abspath('_themes'), settings.theme)
        if os.path.exists(theme):
            loaders.append(theme)
        else:
            loaders.append(
                os.path.join(g.liquid_directory, '_themes', settings.theme)
            )

        jinja = Environment(
            loader=FileSystemLoader(loaders),
            autoescape=False,  # blog don't need autoescape
            extensions=settings.jinja_extensions,
        )
        jinja.globals = settings.jinja_variables
        for k, v in settings.jinja_filters.items():
            jinja.filters.update({k: import_object(v)})

        self._jinja = jinja
        return jinja

    def write(self, content, destination):
        folder = os.path.split(destination)[0]
        # on Mac OSX, `folder` == `FOLDER`
        # then make sure destination is lowercase
        if not os.path.isdir(folder):
            os.makedirs(folder)

        f = open(destination, 'w')
        f.write(content)
        f.close()
        return

    def render(self, params, template, destination):
        tpl = self.jinja.get_template(template)
        html = tpl.render(params)
        self.write(html, destination)
        #: logging
        return


def get_post_slug(post, slug_format):
    regex = re.compile(r'\{\{(.*?)\}\}')

    def replace(m):
        key = m.group(1)
        tokens = key.split('.')
        value = post
        for token in tokens:
            value = getattr(value, token)

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
