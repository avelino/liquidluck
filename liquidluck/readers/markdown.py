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


:copyright: (c) 2012 by Hsiaoming Yang (aka lepture)
:license: BSD
'''


import re
import logging
import misaka as m

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from liquidluck.readers.base import BaseReader, Post
from liquidluck.utils import to_unicode


class MarkdownReader(BaseReader):
    def support_type(self):
        return 'md', 'mkd', 'markdown'

    def render(self):
        f = open(self.filepath)
        logging.info('read ' + self.filepath)
        content = f.read()
        f.close()

        meta_regex = re.compile(
            r"^\s*(?:-|=){3,}\s*\n((?:.|\n)+?)\n\s*(?:-|=){3,}\s*\n*",
            re.MULTILINE
        )
        match = re.match(meta_regex, content)
        if not match:
            logging.error("No metadata in: %s" % self.filepath)
            return None

        meta = match.group(1)
        meta = re.sub(r'\r\n|\r|\n', '\n', meta)
        dct = {}
        k = v = None
        for item in meta.split('\n'):
            item = item.replace('\t', '    ')
            if item.startswith('  ') and k:
                dct[k] = dct[k] + '\n' + item.lstrip()
            if ':' in item and not item.startswith(' '):
                index = item.find(':')
                k, v = item[:index], item[index + 1:]
                k, v = k.rstrip(), v.lstrip()
                dct[k] = to_unicode(v)

        content = markdown(content[match.end():])
        return Post(self.filepath, content, meta=dct)


class JuneRender(m.HtmlRenderer, m.SmartyPants):
    def block_code(self, text, lang):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
        else:
            return '\n<pre><code>%s</code></pre>\n' % escape(text.strip())

        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

    def autolink(self, link, is_email):
        title = link.replace('http://', '').replace('https://', '')

        #: youtube.com
        pattern = r'http://www.youtube.com/watch\?v=([a-zA-Z0-9\-\_]+)'
        match = re.match(pattern, link)
        if not match:
            pattern = r'http://youtu.be/([a-zA-Z0-9\-\_]+)'
            match = re.match(pattern, link)
        if match:
            value = ('<iframe width="560" height="315" src='
                     '"http://www.youtube.com/embed/%(id)s" '
                     'frameborder="0" allowfullscreen></iframe>'
                     '<div><a rel="nofollow" href="%(link)s">'
                     '%(title)s</a></div>'
                    ) % {'id': match.group(1), 'link': link, 'title': title}
            return value

        #: gist support
        pattern = r'(https?://gist.github.com/[\d]+)'
        match = re.match(pattern, link)
        if match:
            value = ('<script src="%(link)s.js"></script>'
                     '<div><a rel="nofollow" href="%(link)s">'
                     '%(title)s</a></div>'
                    ) % {'link': match.group(1), 'title': title}
            return value

        #: vimeo.com
        pattern = r'http://vimeo.com/([\d]+)'
        match = re.match(pattern, link)
        if match:
            value = ('<iframe width="500" height="281" frameborder="0" '
                     'src="http://player.vimeo.com/video/%(id)s" '
                     'allowFullScreen></iframe>'
                     '<div><a rel="nofollow" href="%(link)s">'
                     '%(title)s</a></div>'
                    ) % {'id': match.group(1), 'link': link, 'title': title}
            return value
        if is_email:
            return '<a href="mailto:%(link)s">%(link)s</a>' % {'link': link}

        return '<a href="%s">%s</a>' % (link, title)


def markdown(text):
    text = to_unicode(text)
    render = JuneRender(flags=m.HTML_USE_XHTML)
    md = m.Markdown(
        render,
        extensions=m.EXT_FENCED_CODE | m.EXT_AUTOLINK,
    )
    return md.render(text)


_XHTML_ESCAPE_RE = re.compile('[&<>"]')
_XHTML_ESCAPE_DICT = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}


def escape(value):
    """Escapes a string so it is valid within XML or XHTML."""
    if not isinstance(value, (basestring, type(None))):
        value = value.decode('utf-8')
    return _XHTML_ESCAPE_RE.sub(
        lambda match: _XHTML_ESCAPE_DICT[match.group(0)], value)
