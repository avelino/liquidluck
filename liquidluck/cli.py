#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import liquidluck
from liquidluck.generator import build
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g


DEFAULT_SETTING = """
permalink = '{{category}}/{{filename}}.html'
perpage = 30
feedcount = 20

author = 'admin'  # choose a nickname
authors = {
    'admin': {
        'name': 'Full Name',
        'email': 'admin@example.com',
        'website': 'http://example.com',
    },
}


theme = 'default'
# theme variables are defined by theme creator
theme_variables = {}

# readers = {}
# readers_variables = {}
# writers = {}
# writers_variables = {}

# template_variables = {}
# template_filters = {}
"""


def create(config):
    #: require site information
    site_name = raw_input("Site Name: ")
    site_url = raw_input("Site URL: ")
    code = (
        '#!/usr/bin/env python\n'
        '# -*- coding: utf-8 -*-\n\n'
        "site = {\n"
        '    "name": "%s",\n'
        '    "url": "%s",\n'
        '    # "prefix": "blog",\n'
        '}\n\n'
    ) % (site_name, site_url)

    source = raw_input("What is your directory for posts(content): ")
    source = source or 'content'
    code += "source = '%s'\n" % source
    if not os.path.isdir(source):
        os.makedirs(source)

    output = raw_input("Where is your directory for output(deploy): ")
    output = output or 'deploy'
    code += "output = '%s'\n" % output
    code += "static_output = '%s/static'\n" % output
    code += "static_prefix = '/static/'\n"
    code += DEFAULT_SETTING

    f = open(config, 'w')
    f.write(code)
    f.close()
    print("\nYour site is created.\n\n\n")
    print("Get help: http://liquidluck.readthedocs.org")


def launch_help():
    import webbrowser
    webbrowser.open('http://liquidluck.readthedocs.org')


def __load_themes():
    import time
    import tempfile
    f = os.path.join(tempfile.gettempdir(), 'liquidluck.json')

    def fetch():
        import urllib
        content = urllib.urlopen(
            'http://project.lepture.com/liquidluck/themes.json'
        ).read()
        open(f, 'w').write(content)

    if not os.path.exists(f) or os.stat(f).st_mtime + 600 < time.time():
        fetch()

    content = open(f).read()

    try:
        import json
        json_decode = json.loads
    except ImportError:
        import simplejson
        json_decode = simplejson.loads

    themes = json_decode(content)
    return themes


SEARCH_TEMPLATE = '''
Theme: %(name)s
Author: %(author)s
Homepage: %(homepage)s

'''


def search(keyword=None):
    themes = __load_themes()

    if keyword and keyword not in themes:
        print("Can't find theme: %s" % keyword)
        return None

    if keyword:
        themes = [themes[keyword]]

    for theme in themes:
        theme.update({'name': keyword})
        print(SEARCH_TEMPLATE % theme)
    return


def install(keyword):
    themes = __load_themes()
    if keyword not in themes:
        print("can't find theme %s" % keyword)
        return
    theme = themes[keyword]
    repo = theme['repo']
    output = '_themes/%s' % keyword
    import subprocess
    subprocess.call(['git', 'clone', repo, output])


def main():
    parser = argparse.ArgumentParser(prog='liquidluck')

    subparser = parser.add_subparsers(
        title='available commands', dest='subparser'
    )

    subparser.add_parser(
        'create', help='create a blog repo',
    ).add_argument(
        '-s', '--settings', default='settings.py', help='setting file'
    )

    parser_gen = subparser.add_parser(
        'build', help='build the site'
    )
    parser_gen.add_argument(
        '-v', '--verbose', action='store_true',
        help='show more logging'
    )
    parser_gen.add_argument(
        '-s', '--settings', default='settings.py', help='setting file'
    )

    subparser.add_parser(
        'search', help='search theme'
    ).add_argument('theme', nargs='?', help='theme name')

    subparser.add_parser(
        'install', help='install a theme'
    ).add_argument('theme', nargs='?', help='theme name')

    subparser.add_parser(
        'document', help='launch documentation in browser'
    )

    subparser.add_parser(
        'version', help='show Felix Felicis version'
    )

    parser_webhook = subparser.add_parser(
        'webhook', help='start a webhook server',
    )
    parser_webhook.add_argument(
        'daemon', nargs='?', default='start',
    )
    parser_webhook.add_argument(
        '-p', '--port', nargs='?', default=8000,
        help='server port'
    )

    args = parser.parse_args()

    if args.subparser == 'version':
        print("Felix Felicis Version: %s" % liquidluck.__version__)
        return

    if args.subparser == 'document':
        launch_help()
        return

    if args.subparser == 'search':
        search(args.theme)
        return

    if args.subparser == 'install':
        install(args.theme)
        return

    if args.subparser == 'create':
        create(args.settings)
        return

    if args.subparser == 'webhook':
        from liquidluck.webhook import webhook
        webhook(args.port, args.daemon)
        return

    #: args.subparser == 'build'
    if not os.path.exists(args.settings):
        answer = raw_input(
            "Can't find your setting files, "
            "would you like to create one?(Y/n) "
        )
        if answer.lower() == 'n':
            return
        create(args.settings)
        return

    g.detail_logging = args.verbose
    enable_pretty_logging()
    build(args.settings)


if __name__ == '__main__':
    main()
