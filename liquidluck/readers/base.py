#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Reader, read content, parse to html.

:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''

import datetime
import logging
from liquidluck.options import settings


class BaseReader(object):
    """
    Base Reader, all readers must inherit this module. e.g.:

        ``MarkdownReader(BaseReader)``

    New reader required:
        - ``support_type``
        - ``parse_post``

    New reader optional:
        - ``start``
    """
    def __init__(self, filepath=None):
        self.filepath = filepath

    def start(self):
        return None

    def get_resource_slug(self):
        pass

    def support_type(self):
        return None

    def support(self):
        _type = self.support_type()
        if isinstance(_type, basestring):
            return self.filepath.endswith('.' + _type)
        if isinstance(_type, list) or isinstance(_type, tuple):
            for _t in _type:
                if isinstance(_t, basestring) and \
                   self.filepath.endswith('.' + _t):
                    return True
        return False

    def render(self):
        """rend to post.

        post:
            - public
            - date
            - author
            - title
            - content
            - slug
            - destination
        """
        try:
            post = self.parse_post()
        except Exception as e:
            logging.error(e)
            return None

        if post.get('public', 'true') == 'false':
            post.public = False
        else:
            post.public = True

        if not post.get('date', None) and post.public:
            logging.error('post has no date')
            return None

        if not post.get('author', None):
            post.author = settings.author

        try:
            post.date = self._parse_datetime(post.get('date'))
        except ValueError as e:
            logging.error(e)
            return None

        for key in post.keys():
            if '_date' in key or '_time' in key:
                try:
                    post[key] = self._parse_datetime(post[key])
                except ValueError as e:
                    logging.error(e)
                    return None

        post.destination = self.get_resource_destination()
        post.slug = self.get_resource_slug()
        post.filepath = self.filepath
        return post

    def parse_post(self):
        raise NotImplementedError

    def _parse_datetime(sef, value):
        supported_formats = [
            '%a %b %d %H:%M:%S %Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H:%M',
            '%Y%m%d %H:%M:%S',
            '%Y%m%d %H:%M',
            '%Y-%m-%d',
            '%Y%m%d',
        ]
        for format in supported_formats:
            try:
                return datetime.strptime(value, format)
            except ValueError:
                pass
        logging.error('Unrecognized date/time: %r' % value)
        raise ValueError('Unrecognized date/time: %r' % value)
