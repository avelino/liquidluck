# coding: utf-8
"""
    liquidluck.rst
    ~~~~~~~~~~~~~~

    reStructuredText reader for liquidluck.

    :copyright: (c) 2013 by Hsiaoming Yang
"""

import logging
from xml.dom import minidom
from docutils.core import publish_parts
from ._base import BaseReader
from .._compat import to_unicode

logger = logging.getLogger('liquidluck')


class RstReader(BaseReader):
    filetypes = ['rst']

    def parse(self, text):
        """Parse text into content and meta info.

        A valid markdown article looks like::

            title
            ========

            :date: 2011-09-01
            :category: life
            :tags: tag1, tag2

            Your content here.
        """
        extra_setting = {'initial_header_level': '2'}
        parts = publish_parts(
            text, writer_name='html',
            settings_overrides=extra_setting,
        )
        body = parts['body']
        meta = parse_meta(parts['docinfo'])
        meta['title'] = parts['title']
        return body, meta


def parse_meta(html):
    content = html.replace('\n', '')
    if not content:
        return {}

    docinfo = {}
    dom = minidom.parseString(to_unicode(content).encode('utf-8'))
    for node in dom.getElementsByTagName('tr'):
        key, value = _node_to_pairs(node)
        docinfo[key] = value
    return docinfo


def _node_to_pairs(node):
    '''
    parse docinfo to python object

    <tr><th class="docinfo-name">Date:</th>
    <td>2011-10-12</td></tr>
    '''
    keyNode = node.firstChild
    key = _plain_text(keyNode)
    key = key.lower().rstrip(':')

    valueNode = node.lastChild

    tag = valueNode.firstChild.nodeName
    if 'ul' == tag or 'ol' == tag:
        value = []
        for node in valueNode.getElementsByTagName('li'):
            value.append(_plain_text(node))
    else:
        value = _plain_text(valueNode)
    return key, value


def _plain_text(node):
    child = node.firstChild
    if not child:
        return None
    if child.nodeType == node.TEXT_NODE:
        return to_unicode(child.data)

    return None
