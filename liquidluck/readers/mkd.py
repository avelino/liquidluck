#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Blog content file parser.

Syntax::

    -----------------
    title: Title
    date: 2011-09-01
    folder: life
    tags: tag1, tag2
    -----------------

    Your content here. And it support code highlight.

    ```python

    def hello():
        return 'Hello World'

    ```


:copyright: (c) 2011 by Hsiaoming Young (aka lepture)
:license: BSD
'''


import re
import misaka as m
import houdini as h

from misaka import HtmlRenderer
from misaka import SmartyPants

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
# from markdown import Markdown

from liquidluck.readers import Reader
from liquidluck.namespace import ns, NameSpace
from liquidluck.utils import to_unicode, import_module
from liquidluck import logger

if ns.site.syntax == 'class':
    INLINESTYLES = False
else:
    INLINESTYLES = True

"""
```python
def yourcode():
    print('here')
```
"""


markdown_prefork = NameSpace({
    'youku': 'liquidluck.filters.youku',
    'tudou': 'liquidluck.filters.tudou',
    'yinyuetai': 'liquidluck.filters.yinyuetai',
})


class BleepRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(noclasses=INLINESTYLES)
        return highlight(text, lexer, formatter)

    def preprocess(self, text):
        if 'markdown_prefork' in ns.sections:
            markdown_prefork.update(ns.sections.markdown_prefork)

        for module in markdown_prefork.values():
            if module:
                text = import_module(module)(text)

        return text


renderer = BleepRenderer()


def markdown(text):
    md = m.Markdown(
        renderer,
        extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS
    )
    return md.render(text)


class MarkdownParser(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        f = open(self.filepath)
        logger.info('read ' + self.filepath)
        content = f.read()
        f.close()

        meta_regex = re.compile(
            r"^\s*(?:-|=){3,}\s*\n((?:.|\n)+?)\n\s*(?:-|=){3,}\s*\n*",
            re.MULTILINE
        )
        match = re.match(meta_regex, content)
        if not match:
            logger.error("No metadata in: %s" % self.filepath)
            return None
        meta = match.group(1)
        meta = re.sub(r'\r\n|\r|\n', '\n', meta)
        dct = {}
        k = v = None
        for meta in meta.split('\n'):
            meta = meta.replace('\t', '    ')
            if meta.startswith('  ') and k:
                dct[k] = dct[k] + '\n' + meta.lstrip()
            if ':' in meta and not meta.startswith(' '):
                index = meta.find(':')
                k, v = meta[:index], meta[index + 1:]
                k, v = k.rstrip(), v.lstrip()
                dct[k] = to_unicode(v)
        text = to_unicode(content[match.end():])
        dct['content'] = markdown(text)
        return dct


class MarkdownReader(Reader):
    def support_type(self):
        return 'md', 'mkd', 'markdown'

    def parse_post(self):
        if hasattr(self, 'post'):
            return self.post
        parts = MarkdownParser(self.filepath).read()

        post = NameSpace(parts)
        tags = post.get('tags', None)
        if tags:
            post.tags = [tag.strip() for tag in tags.split(',')]
        self.post = post
        return post
