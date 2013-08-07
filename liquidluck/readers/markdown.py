# coding: utf-8
"""
    liquidluck.markdown
    ~~~~~~~~~~~~~~~~~~~

    Markdown reader for liquidluck.

    :copyright: (c) 2013 by Hsiaoming Yang
"""

import re
import logging
import misaka as m
from ._base import BaseReader

logger = logging.getLogger('liquidluck')


class MarkdownReader(BaseReader):
    filetypes = ['md', 'mkd', 'markdown']

    def parse(self, text):
        """Parse text into content and meta info.

        A valid markdown article looks like::

            # This is the title

            - date: 2012-12-11
            - metakey: meta value

            Here is the description.

            ----------

            Under this are the content.
        """
        headers = []
        body = []
        recording = True

        for line in text.splitlines():
            if recording and line.startswith('---'):
                recording = False
            if recording:
                headers.append(line)
            else:
                body.append(line)

        content = parse_content('\n'.join(body))
        meta = parse_meta('\n'.join(headers))
        return content, meta


def parse_meta(text):
    html = m.html(text)
    titles = re.findall(r'<h1>(.*)</h1>', html)

    if not titles:
        logger.error('Title not found.')
        title = None
    else:
        title = titles[0]

    meta = {'title': title}
    items = re.findall(r'<li>(.*?)</li>', html, re.S)
    for item in items:
        index = item.find(':')
        key = item[:index].rstrip()
        value = item[index + 1:].lstrip()
        meta[key] = value

    desc = re.findall(r'<p>(.*?)</p>', html, re.S)
    if desc:
        meta['description'] = '\n\n'.join(desc)
    return meta


def parse_content(text):
    #TODO
    return m.html(text)
