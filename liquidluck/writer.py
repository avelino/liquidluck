#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Writer, write your content to html.

:copyright: (c) 2011 by Hsiaoming Young (aka lepture)
:license: BSD
'''


import os
import datetime
import shutil
from math import log
from fnmatch import fnmatch
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import Environment, FileSystemLoader

from liquidluck.reader import restructuredtext

from liquidluck import logger


builtin_templates = os.path.join(os.path.dirname(__file__), 'templates')

class Writer(object):
    _jinja_context = {}
    _jinja_filters = {}

    def __init__(self, config, projectdir):
        self.config = config
        self.projectdir = projectdir

        tpl = os.path.join(projectdir, config.site.get('template', 'templates'))
        self.jinja = Environment(
            loader = FileSystemLoader([tpl, builtin_templates]),
            autoescape = config.site.get('autoescape', False),
            extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        )

        # init
        self.register_context('context', config.context)
        self.register_filter('restructuredtext', restructuredtext)

    @property
    def postdir(self):
        _dir = self.config.get('postdir', 'content')
        return os.path.join(self.projectdir, _dir)

    @property
    def deploydir(self):
        _dir = self.config.get('deploydir', 'deploy')
        return os.path.join(self.projectdir, _dir)

    @property
    def staticdir(self):
        _dir = self.config.get('staticdir', '_static')
        return os.path.join(self.projectdir, _dir)

    @classmethod
    def register_context(cls, key, value):
        cls._jinja_context[key] = value
        return cls

    @classmethod
    def register_filter(cls, key, value):
        cls._jinja_filters[key] = value
        return cls

    def render(self, template, context={}):
        context.update(self._jinja_context)
        self.jinja.filters.update(self._jinja_filters)
        tpl = self.jinja.get_template(template)
        return tpl.render(context)


    def make_dest_folder(self, dest):
        folder = os.path.split(dest)[0]
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return folder

    def copy_to(self, source, dest):
        self.make_dest_folder(dest)
        if not os.path.exists(dest):
            logger.info('copy ' + source)
            shutil.copy(source, dest)
            return True
        return False

    def sort_rsts(self, rsts, reverse=True):
        return sorted(rsts, key=lambda rst: rst.get_info('date'), reverse=reverse)

    def walk(self, dest):
        for root, dirs, files in os.walk(dest):
            for f in files:
                path = os.path.join(root, f)
                yield path

    def write(self, params, tpl, dest):
        dest = os.path.join(self.deploydir, dest)
        logger.info('write ' + dest)
        self.make_dest_folder(dest)
        f = open(dest, 'w')
        html = self.render(tpl, params)
        f.write(html.encode('utf-8'))
        f.close()
        return 

    def register(self):
        pass

    def run(self):
        pass
