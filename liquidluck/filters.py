#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from liquidluck.utils import to_unicode


def xmldatetime(value):
    """ this is a jinja filter """
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


def embed(value):
    """ this filter only avaible for markdown """

    #youtube
    value = re.sub(
        r'http://www.youtube.com/watch\?v=([a-zA-Z0-9\-\_]+)',
        r'<div><embed src="http://www.youtube.com/v/\1?fs=1&amp;hl=en_US" '
        r'type="application/x-shockwave-flash" allowscriptaccess="always" '
        r'allowfullscreen="true" width="480" height="385" />'
        r'<br /><small><a rel="nofollow" href="http://youtu.be/\1">'
        r'http://youtu.be/\1</a></small></div>',
        value)
    #youtube
    value = re.sub(
        r'http://youtu.be/([a-zA-Z0-9\-\_]+)',
        r'<div><embed src="http://www.youtube.com/v/\1?fs=1&amp;hl=en_US" '
        r'type="application/x-shockwave-flash" allowscriptaccess="always" '
        r'allowfullscreen="true" width="480" height="385" />'
        r'<br /><small><a rel="nofollow" href="http://youtu.be/\1">'
        r'http://youtu.be/\1</a></small></div>',
        value)
    #youku
    value = re.sub(
        r'http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html',
        r'<div><embed src="http://player.youku.com/player.php/sid/\1/v.swf" '
        r'quality="high" width="480" height="400" '
        r'allowScriptAccess="sameDomain" type="application/x-shockwave-flash"'
        r'/><br /><small><a rel="nofollow" '
        r'href="http://v.youku.com/v_show/id_\1.html">'
        r'http://v.youku.com/v_show/id_\1.html</a></small></div>',
        value)
    #tudou
    value = re.sub(
        r'http://www.tudou.com/programs/view/([a-zA-z0-9\-\=]+)/',
        r'<div><embed src="http://www.tudou.com/v/\1/v.swf" width="480" '
        r'height="400" allowScriptAccess="sameDomain" wmode="opaque" '
        r'type="application/x-shockwave-flash" /><br />'
        r'<small><a rel="nofollow" '
        r'href="http://www.tudou.com/programs/view/\1/">'
        r'http://www.tudou.com/programs/view/\1/</a></small></div>',
        value)
    #yinyuetai
    value = re.sub(
        r'http://www.yinyuetai.com/video/(\d+)',
        r'<div><embed src="http://www.yinyuetai.com/video/player/\1/v_0.swf"'
        r'quality="high" width="480" height="334" align="middle" '
        r'allowScriptAccess="sameDomain" type="application/x-shockwave-flash">'
        r'</embed><br /><small><a rel="nofollow" '
        r'href="http://www.yinyuetai.com/video/\1">'
        r'http://www.yinyuetai.com/video/\1</a></small></div>',
        value)
    return value


def remove_linebreak_for_double_width_language(value):
    """This will remove linebreak for double width languages.
    """
    pattern = re.compile(
        r'([^a-zA-Z0-9!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`\{\|\}~])'
        r'(\n|\r\n|\r)'
        r'([^a-zA-Z0-9!\"#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`\{\|\}~])'
    )
    return pattern.sub(r'\1\3', value)


def first_paragraph(value):
    regex = re.compile(r'<p>(.*?)</p>', re.U|re.S)
    m = regex.findall(value)
    if not m:
        return ''
    return '<p>%s</p>' % m[0]
