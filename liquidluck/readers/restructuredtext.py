#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Blog content file parser.

Syntax::

    title
    ========

    :date: 2011-09-01
    :category: life
    :tags: tag1, tag2

    Your content here. And it supports code highlight.

    Example::

        .. sourcecode:: python

            def hello():
                return 'hello'

:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''

import logging
from xml.dom import minidom
from docutils import nodes
from docutils.core import publish_parts
from docutils.parsers.rst import directives, Directive
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from liquidluck.readers.base import BaseReader
from liquidluck.options import settings
from liquidluck.utils import to_unicode, utf8


class RestructuredTextReader(BaseReader):
    SUPPORT_TYPE = ['rst', 'rst.txt', 'restructuredtext']

    def render(self):
        f = open(self.filepath)
        logging.debug('read ' + self.relative_filepath)

        content = f.read()
        f.close()

        extra_setting = {'initial_header_level': '2'}
        parts = publish_parts(
            content, writer_name='html',
            settings_overrides=extra_setting,
        )
        title = parts['title']
        body = parts['body']
        meta = parts['docinfo']

        meta = self._parse_meta(meta)
        return self.post_class(self.filepath, body, title=title, meta=meta)

    def _parse_meta(self, meta):
        content = meta.replace('\n', '')
        if not content:
            return {}

        docinfo = {}
        dom = minidom.parseString(utf8(content))
        for node in dom.getElementsByTagName('tr'):
            key, value = self._node_to_pairs(node)
            docinfo[key] = value
        return docinfo

    def _plain_text(self, node):
        child = node.firstChild
        if not child:
            return None
        if child.nodeType == node.TEXT_NODE:
            return to_unicode(child.data)

        return None

    def _node_to_pairs(self, node):
        '''
        parse docinfo to python object

        <tr><th class="docinfo-name">Date:</th>
        <td>2011-10-12</td></tr>
        '''
        keyNode = node.firstChild
        key = self._plain_text(keyNode)
        key = key.lower().rstrip(':')

        valueNode = node.lastChild

        tag = valueNode.firstChild.nodeName
        if 'ul' == tag or 'ol' == tag:
            value = []
            for node in valueNode.getElementsByTagName('li'):
                value.append(self._plain_text(node))
        else:
            value = self._plain_text(valueNode)
        return key, value


INLINESTYLES = settings.get('highlight_inline', False)
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)
VARIANTS = {
    'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}


class Pygments(Directive):
    """ Source code syntax hightlighting.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given

        formatter = self.options and VARIANTS[self.options.keys()[0]] \
                or DEFAULT
        parsed = highlight('\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

directives.register_directive('sourcecode', Pygments)
directives.register_directive('code-block', Pygments)
