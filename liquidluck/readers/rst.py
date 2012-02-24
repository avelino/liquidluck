#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Blog content file parser.

Syntax::

    title
    ========

    :date: 2011-09-01
    :folder: life
    :tags:
        - tag1
        - tag2

    Your content here. And it support code highlight.

    Example::

        .. sourcecode:: python

            def hello():
                return 'hello'

:copyright: (c) 2011 by Hsiaoming Young (aka lepture)
:license: BSD
'''

from xml.dom import minidom
from docutils import nodes
from docutils.core import publish_parts
from docutils.parsers.rst import directives, Directive
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer

from liquidluck import logger
from liquidluck.readers import Reader
from liquidluck.utils import to_unicode
from liquidluck.namespace import ns, NameSpace

if ns.site.syntax == 'class':
    INLINESTYLES = False
else:
    INLINESTYLES = True
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)
VARIANTS = {
    'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}


class Pygments(Directive):
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

directives.register_directive('code-block', Pygments)
directives.register_directive('sourcecode', Pygments)


def restructuredtext(content):
    """
    this is a jinja filter.
    """
    extra_setting = {'initial_header_level': '3'}
    parts = publish_parts(
        content, writer_name='html',
        settings_overrides=extra_setting,
    )
    return parts['body']


class rstParser(object):
    def __init__(self, filepath):
        self.filepath = filepath

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
        key = key.lower().replace(':', '')

        valueNode = node.lastChild

        tag = valueNode.firstChild.nodeName
        if 'ul' == tag or 'ol' == tag:
            value = []
            nodes = valueNode.getElementsByTagName('li')
            for node in nodes:
                value.append(self._plain_text(node))
        else:
            value = self._plain_text(valueNode)
        return key, value

    def read(self):
        f = open(self.filepath)
        logger.info('read ' + self.filepath)
        content = f.read()
        f.close()

        extra_setting = {'initial_header_level': '2'}
        parts = publish_parts(
            content, writer_name='html',
            settings_overrides=extra_setting,
        )

        # get docinfo
        docinfo = []
        content = parts['docinfo'].replace('\n', '')
        if not content:
            return parts

        dom = minidom.parseString(content.encode('utf-8'))
        nodes = dom.getElementsByTagName('tr')
        for node in nodes:
            docinfo.append(self._node_to_pairs(node))

        parts['docinfo'] = docinfo
        return parts


class RstReader(Reader):
    def support_type(self):
        return 'rst'

    def parse_post(self):
        if hasattr(self, 'post'):
            return self.post

        parts = rstParser(self.filepath).read()
        docinfo = dict(parts['docinfo'])

        post = NameSpace()
        for k, v in docinfo.items():
            post[k] = v
        post.title = parts['title']
        post.content = parts['body']
        self.post = post
        return post
