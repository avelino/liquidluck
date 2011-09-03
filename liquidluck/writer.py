#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from fnmatch import fnmatch
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import Environment, FileSystemLoader, Markup
from reader import rstReader

import log


builtin_templates = os.path.join(os.path.dirname(__file__), 'templates')


class Writer(object):
    def __init__(self, config, projectdir):
        self.config = config
        self.projectdir = projectdir
        self.stacks = []
        self.folders = []
        self.years = []

        tpl = os.path.join(projectdir, config.site.get('template', 'templates'))
        self.jinja = Environment(
            loader = FileSystemLoader([tpl, builtin_templates]),
            autoescape = config.site.get('autoescape', False),
            extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        )

    @property
    def postdir(self):
        _dir = self.config.get('postdir', 'content')
        return os.path.join(self.projectdir, _dir)

    @property
    def deploydir(self):
        _dir = self.config.get('deploydir', 'deploy')
        return os.path.join(self.projectdir, _dir)

    def walk(self):
        for root, dirs, files in os.walk(self.postdir):
            for f in files:
                yield os.path.join(root, f)

    def calc(self):
        for f in self.walk():
            print f
            rst = rstReader(f).render_rst()
            docinfo = rst['docinfo']
            folder = docinfo.get('folder', None)
            if folder:
                self.folders = yield folder, rst

            self.stacks = yield rst


    def mkdir_dest_folder(self, folder=None):
        if folder:
            dest = os.path.join(self.deploydir, folder)
        else:
            dest = os.path.join(self.deploydir)
        if not os.path.isdir(dest):
            os.makedirs(dest)
        return dest
    

    def write_post(self, rst_parts):
        docinfo = dict(rst_parts['docinfo'])
        public = docinfo.get('public', 'true')
        if 'false' == public.lower():
            return # this is a secret post

        folder = docinfo.get('folder', None)
        self.mkdir_dest_folder(folder)

        _path = rst_parts['file'].naked_slug + '.html'
        dest = os.path.join(self.deploydir, _path)
        f = open(dest, 'w')
        _tpl = docinfo.get('tpl', 'post.html')
        html = self._jinja_render(_tpl, {'rst': rst_parts})
        f.write(html)
        f.close()
        return 

    def write_archive(self, rsts, dest='archive.html'):
        folders = dest.split('/')
        if len(folders) > 1:
            folder = '/'.join(folders[:-1])
            self.mkdir_dest_folder(folder)
        dest = os.path.join(self.deploydir, dest)



    def _jinja_render(self, template, context={}):
        prepare = {'site': self.config.site, 'context': self.config.context}
        context.update(prepare)
        tpl = self.jinja.get_template(template)
        return tpl.render(context)


