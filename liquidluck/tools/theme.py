#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from liquidluck.options import g
from liquidluck.utils import to_unicode, utf8


def __fetch_themes():
    import urllib
    if hasattr(urllib, 'urlopen'):
        urlopen = urllib.urlopen
    else:
        import urllib.request
        urlopen = urllib.request.urlopen

    content = urlopen(
        "https://api.github.com/legacy/repos/search/%22liquidluck-theme-%22"
    ).read()
    content = to_unicode(content)
    return content


def __filter_themes(content):
    try:
        import json
        json_decode = json.loads
    except ImportError:
        import simplejson
        json_decode = simplejson.loads

    repos = json_decode(content)
    themes = {}
    if 'repositories' not in repos and 'message' in repos:
        print(repos['message'])
        return {}
    for theme in repos['repositories']:
        fork = theme['fork']
        if not fork:
            name = theme['name'].replace('liquidluck-theme-', '')
            name = name.strip().strip('-')
            theme['name'] = name
            themes[name] = theme
    return themes


def __load_themes(force=False):
    import time
    import tempfile
    path = os.path.join(tempfile.gettempdir(), 'liquidluck.json')

    if not os.path.exists(path) or \
       os.stat(path).st_mtime + 600 < time.time() or \
       force:
        content = __fetch_themes()
        if "repositories" not in content:
            return content
        f = open(path, 'w')
        f.write(utf8(content))
        f.close()

    content = to_unicode(open(path).read())
    return __filter_themes(content)


SEARCH_TEMPLATE = '''
Theme: %(name)s
Author: %(username)s
Description: %(description)s
Updated: %(pushed)s
Status: %(forks)s forks | %(followers)s followers
URL: https://github.com/%(username)s/liquidluck-theme-%(name)s
'''


def search(keyword=None, clean=False, force=False):
    themes = __load_themes(force)
    available = {}

    if keyword:
        for name in themes:
            if keyword in name:
                available[name] = themes[name]

    for name in (available or themes):
        if clean:
            print(name)
        else:
            theme = themes[name]
            print(SEARCH_TEMPLATE % theme)
    return


def install(keyword=None, widely=False):
    if not keyword:
        print("You need specify a theme")
        return
    if '/' in keyword:
        user, name = keyword.split('/')
        if not name:
            keyword = user
            name = 'liquidluck-theme'
        elif name.startswith('liquidluck-theme-'):
            keyword = name.replace('liquidluck-theme-', '', 1)
        else:
            keyword = name
            name = 'liquidluck-theme-%s' % name

        repo = 'git://github.com/%s/%s' % (user, name)
    else:
        themes = __load_themes()
        if keyword not in themes:
            print("can't find theme %s" % keyword)
            return
        theme = themes[keyword]
        repo = 'https://github.com/%(username)s/liquidluck-theme-%(name)s' \
                % theme
    if widely:
        output = os.path.join(g.theme_gallery, keyword)
    else:
        output = '_themes/%s' % keyword
    import subprocess
    if os.path.exists(output):
        subprocess.call(['git', 'pull'], cwd=output)
    else:
        subprocess.call(['git', 'clone', repo, output])


if __name__ == '__main__':
    search()
