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

from jinja2 import Environment, FileSystemLoader

from liquidluck.utils import import_module
from liquidluck.namespace import ns

from liquidluck import logger


def make_folder(dest):
    folder = os.path.split(dest)[0]
    # on Mac OSX, `folder` == `FOLDER`
    # then make sure dest is lowercase
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


def copy_to(source, dest):
    if os.path.exists(dest) and \
       os.stat(source).st_mtime < os.stat(dest).st_mtime:
        logger.info('Ignore ' + source)
        return False
    make_folder(dest)
    logger.info('copy ' + source)
    shutil.copy(source, dest)
    return True


def sort_posts(posts, reverse=True):
    return sorted(posts, key=lambda post: post.date, reverse=reverse)


class Writer(object):
    """
    All Writers must inherit this class. e.g. StaticWriter(Writer)

    All Writers must has ``run()`` function.
    """
    first_runing = True
    writer_type = 'Writer'

    def __init__(self):
        logger.info('Load Writer: %s' % self.writer_type)

    def start(self):
        return

    @property
    def jinja(self):
        if hasattr(self, '_jinja'):
            return self._jinja
        tpl = os.path.join(ns.storage.projectdir,
                           ns.site.template)
        autoescape = ns.site.autoescape == 'true'
        jinja = Environment(
            loader=FileSystemLoader([
                tpl, os.path.join(ns.storage.root, '_templates')
            ]),
            autoescape=autoescape,
            extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_'],
        )
        for k, v in ns.filters.items():
            jinja.filters.update({k: import_module(v)})

        self._jinja = jinja
        return jinja

    @property
    def postdir(self):
        return os.path.join(
            ns.storage.projectdir, ns.site.postdir)

    @property
    def deploydir(self):
        return os.path.join(
            ns.storage.projectdir, ns.site.deploydir)

    @property
    def staticdir(self):
        return os.path.join(ns.storage.projectdir,
                            ns.site.staticdir)

    def render(self, template, params={}):
        params.update(dict(ns.storage.functions))
        params.update(dict(ns.data))
        params.update({'context': ns.context})
        params.update({'status': ns.storage.status})
        params.update({'now': datetime.datetime.now()})
        tpl = self.jinja.get_template(template)
        return tpl.render(params)

    def write(self, params, tpl, dest):
        dest = os.path.join(self.deploydir, dest.lower())
        logger.info('write ' + dest)
        make_folder(dest)
        f = open(dest, 'w')
        html = self.render(tpl, params)
        f.write(html.encode('utf-8'))
        f.close()
        return

    def run(self):
        raise NotImplementedError


class FeedMixin(object):
    def write_feed(self, posts, dest='feed.xml', **params):
        count = int(ns.site.feed_count)
        posts = posts[:count]
        _tpl = ns.site.feed_template
        _tpl = params.pop('tpl', _tpl)
        params.update({'posts': posts})
        return self.write(params, _tpl, dest)


class Pagination(object):
    def __init__(self, posts, perpage=30):
        self.allposts = [post for post in posts]
        self.total = len(self.allposts)
        self.pages = (self.total - 1) / perpage + 1
        self.perpage = perpage

    def get_current_page(self, page=1):
        start = (page - 1) * self.perpage
        end = page * self.perpage
        self.posts = self.allposts[start:end]
        if page < self.pages:
            self.next = str(page + 1)
        else:
            self.next = None
        if page > 1:
            self.prev = str(page - 1)
        else:
            self.prev = None
        self.page = page
        return self


class PagerMixin(object):
    def write_pager(self, posts, dest='index.html', **params):
        perpage = int(ns.site.perpage)
        paginator = Pagination(posts, perpage)
        _tpl = ns.site.archive_template
        _tpl = params.pop('tpl', _tpl)

        # first page
        folder, filename = os.path.split(dest)
        if filename == 'index.html' or \
           filename == ns.site.index:
            sub_folder = 'page'
        else:
            sub_folder, ext = os.path.splitext(filename)

        pager = paginator.get_current_page(1)
        pager.folder = folder
        pager.sub_folder = sub_folder

        params.update({'pager': pager})
        self.write(params, _tpl, dest)

        for p in range(paginator.pages):
            dest = os.path.join(folder, sub_folder, '%s.html' % (p + 1))
            pager = paginator.get_current_page(p + 1)
            pager.folder = folder
            self.write(params, _tpl, dest)
