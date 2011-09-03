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

        tpl = os.path.join(projectdir, config.site.get('template', 'templates'))
        self.jinja = Environment(
            loader = FileSystemLoader([tpl, builtin_templates]),
            autoescape = config.site.get('autoescape', False),
            extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        )

    @property
    def postdir(self):
        return os.path.join(self.projectdir, 'content')

    @property
    def deploydir(self):
        return os.path.join(self.projectdir, 'deploy')

    def walk(self):
        for root, dirs, files in os.walk(self.postdir):
            for f in files:
                yield os.path.join(root, f)


    def mkdir_dest_folder(self, folder=None):
        if folder:
            dest = os.path.join(self.deploydir, folder)
        else:
            dest = os.path.join(self.deploydir)
        if not os.path.isdir(dest):
            os.makedirs(dest)
        return dest

    def post_dest(self, filepath, folder=None):
        name = filepath.split('/')[-1]
        name = name.replace('rst', 'html')
        if folder:
            dest = os.path.join(self.deploydir, folder, name)
        else:
            dest = os.path.join(self.deploydir, name)
        return dest

    def write_post(self, filepath):
        rst = rstReader(filepath)
        rst_parts = rst.render_rst()
        docinfo = dict(rst_parts['docinfo'])
        public = docinfo.get('public', 'true')
        if 'false' == public.lower():
            log.warn(filepath)
            return # this is a secret post

        folder = docinfo.get('folder', None)
        self.mkdir_dest_folder(folder)

        f = open(self.post_dest(filepath, folder), 'w')
        html = self._jinja_render('post.html', {'rst': rst_parts})
        f.write(html)
        f.close()
        log.info(filepath)
        return self._calc(filepath, rst)

    def write_archive(self, rsts, dest='archive.html'):
        folders = dest.split('/')
        if len(folders) > 1:
            folder = '/'.join(folders[:-1])
            self.mkdir_dest_folder(folder)
        dest = os.path.join(self.deploydir, dest)

    def _calc(self, filepath, rst):
        pass

    def _jinja_render(self, template, context={}):
        prepare = {'site': self.config.site, 'context': self.config.context}
        context.update(prepare)
        tpl = self.jinja.get_template(template)
        return tpl.render(context)


