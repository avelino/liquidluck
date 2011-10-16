#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from markdown.preprocessors import Preprocessor
from markdown import Markdown

from liquidluck.readers import Reader
from liquidluck.ns import NameSpace
from liquidluck.utils import to_unicode
from liquidluck import logger

INLINESTYLES = False

"""
[sourcecode:lexer]
some code
[/sourcecode]
"""

class CodeBlockPreprocessor(Preprocessor):

    pattern = re.compile(
        r'\[sourcecode:(.+?)\](.+?)\[/sourcecode\]', re.S)

    formatter = HtmlFormatter(noclasses=INLINESTYLES)

    def run(self, lines):
        def repl(m):
            try:
                lexer = get_lexer_by_name(m.group(1))
            except ValueError:
                lexer = TextLexer()
            code = highlight(m.group(2), lexer, self.formatter)
            code = code.replace('\n\n', '\n&nbsp;\n').replace('\n', '<br />')
            return '\n\n<div class="code">%s</div>\n\n' % code
        return self.pattern.sub(repl, ''.join(lines))

md = Markdown()
#md.preprocessors["sourcecode"] = CodeBlockPreprocessor(md)
#TODO code block

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
        tmp = {}
        for meta in meta.split('\n'):
            k, v = meta.split(':')
            k, v = k.rstrip(), v.lstrip()
            tmp[k] = to_unicode(v)
        text = to_unicode(content[match.end():])
        tmp['content'] = md.convert(text)
        return tmp

class MarkdownReader(Reader):
    def support_type(self):
        return 'md', 'mkd', 'markdown'

    def parse_post(self):
        if hasattr(self, 'post'):
            return self.post
        parts = MarkdownParser(self.filepath).read()

        post = NameSpace(parts)
        create_date = post.get('date', None)
        if not create_date:
            logger.error(self.filepath + ' no create date')
            return None
        post.date = datetime.datetime.strptime(create_date, '%Y-%m-%d')
        tags = post.get('tags', None)
        if tags:
            post.tags = [tag.strip() for tag in tags.split(',')]
        if post.get('public', 'true') == 'false':
            post.public = False
        else:
            post.public = True
        self.post = post
        return post
