# -*- coding: utf-8 -*-
'''
Blog config file parser.

Your blog config file must be named as .config, and use a ini syntax.

A example of your config file::

    [site]
    postdir = content
    deploydir = deploy
    ignore = *tmp* *test*
    staticdir = static
    static_prefix = http://static.lepture.com
    template = templates
    archive_template = archive.html
    feed_template = feed.xml
    tagcloud_template = tagcloud.html

    [context]
    sitename = Just lepture
    siteurl = http://lepture.com


:copyright: (c) 2011 by Hsiaoming Young (aka lepture)
:license: BSD
'''

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

class Temp(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

class Config(object):
    def __init__(self, filepath):
        self.config = ConfigParser()
        self.config.read(filepath)

    def get(self, key, value=None):
        return self.site.get(key, value)

    @property
    def site(self):
        return Temp(self.config.items('site'))

    @property
    def context(self):
        return Temp(self.config.items('context'))
