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
    NameSpacelate = NameSpacelates
    archive_NameSpacelate = archive.html
    feed_NameSpacelate = feed.xml
    tagcloud_NameSpacelate = tagcloud.html

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

from liquidluck.ns import NameSpace

class Config(object):
    def __init__(self, filepath):
        self.config = ConfigParser()
        self.config.read(filepath)

    def get(self, key, value=None):
        return self.site.get(key, value)

    @property
    def site(self):
        return NameSpace(self.config.items('site'))

    @property
    def context(self):
        return NameSpace(self.config.items('context'))

    @property
    def writers(self):
        return NameSpace(self.config.items('writers'))

    @property
    def filters(self):
        return NameSpace(self.config.items('filters'))
