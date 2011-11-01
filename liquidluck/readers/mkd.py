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

    [sourcecode:python]

    def hello():
        return 'Hello World'

    [/sourcecode]


:copyright: (c) 2011 by Hsiaoming Young (aka lepture)
:license: BSD
'''


import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from markdown import Markdown

from liquidluck.readers import Reader
from liquidluck.ns import namespace, NameSpace
from liquidluck.utils import to_unicode
from liquidluck.filters import embed
from liquidluck import logger

if namespace.site.get('syntax', 'class') == 'class':
    INLINESTYLES = False
else:
    INLINESTYLES = True

"""
[sourcecode:lexer]
some code
[/sourcecode]
"""

def codeblock(text):
    pattern = re.compile(
        r'\[sourcecode:(.+?)\](.+?)\[/sourcecode\]', re.S)
    formatter = HtmlFormatter(noclasses=INLINESTYLES)
    def repl(m):
        try:
            lexer = get_lexer_by_name(m.group(1))
        except ValueError:
            lexer = TextLexer()
        code = highlight(m.group(2), lexer, formatter)
        code = code.replace('\n\n', '\n&nbsp;\n').replace('\n', '<br />')
        return '\n\n<div class="code">%s</div>\n\n' % code
    return pattern.sub(repl, text)

def markdown(text):
    text = codeblock(text)
    text = embed(text)
    md = Markdown()
    return md.convert(text)

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
                k, v = meta[:index], meta[index+1:]
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
