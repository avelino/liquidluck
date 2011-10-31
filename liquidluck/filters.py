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
    value = re.sub(r'http://www.youtube.com/watch\?v=([a-zA-Z0-9\-\_]+)', r'<small><a rel="nofollow" href="http://youtu.be/\1">Youtube Source</a></small><br /><embed src="http://www.youtube.com/v/\1?fs=1&amp;hl=en_US" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="480" height="385" />', value)
    #youtube
    value = re.sub(r'http://youtu.be/([a-zA-Z0-9\-\_]+)', r'<small><a rel="nofollow" href="http://youtu.be/\1">Youtube Source</a></small><br /><embed src="http://www.youtube.com/v/\1?fs=1&amp;hl=en_US" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="480" height="385" />', value)
    #youku
    value = re.sub(r'http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html', r'<small><a rel="nofollow" href="http://v.youku.com/v_show/id_\1.html">Youku Source</a></small><br /><embed src="http://player.youku.com/player.php/sid/\1/v.swf" quality="high" width="480" height="400" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" />', value)
    #tudou
    value = re.sub(r'http://www.tudou.com/programs/view/([a-zA-z0-9\-\=]+)/',r'<small><a rel="nofollow" href="http://www.tudou.com/programs/view/\1/">Tudou Source</a></small><br /><embed src="http://www.tudou.com/v/\1/v.swf" width="480" height="400" allowScriptAccess="sameDomain" wmode="opaque" type="application/x-shockwave-flash" />', value)
    return value



def first_paragraph(value):
    regex = re.compile(r'<p>(.*?)</p>', re.U|re.S)
    m = regex.findall(value)
    if not m:
        return ''
    return '<p>%s</p>' % m[0]
