#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import logging
import liquidluck
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings
from liquidluck.utils import import_object, walk_dir

from liquidluck.writers.base import load_jinja


def load_settings(path):
    config = {}
    execfile(path, {}, config)

    for key in config:
        setting = config[key]
        if isinstance(setting, dict):
            settings[key].update(setting)
        else:
            settings[key] = setting

    g.output_directory = os.path.abspath(settings.output)
    g.static_directory = os.path.abspath(settings.static_output)
    logging.info('Load Settings Finished')


def load_posts(path):
    g.source_directory = path
    readers = []
    for name in settings.readers:
        reader = settings.readers[name]
        if reader:
            readers.append(import_object(reader))

    def detect_reader(filepath):
        for Reader in readers:
            reader = Reader(filepath)
            if reader.support():
                return reader.run()
        return None

    for filepath in walk_dir(path):
        post = detect_reader(filepath)
        if not post:
            g.pure_files.append(filepath)
        elif not post.date:
            g.pure_pages.append(post)
        elif post.public:
            g.public_posts.append(post)
        else:
            g.secure_posts.append(post)

    g.public_posts = sorted(g.public_posts, key=lambda o: o.date, reverse=True)
    g.secure_posts = sorted(g.secure_posts, key=lambda o: o.date, reverse=True)

    logging.info('Load Posts Finished')


def write_posts():
    writers = []
    for name in settings.writers:
        writer = settings.writers[name]
        if writer:
            writers.append(import_object(writer)())

    load_jinja()

    for writer in writers:
        writer.run()


def generate(config='settings.py'):
    load_settings(config)
    load_posts(g.source_directory)
    write_posts()


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
        '}\n\n'
    ) % (site_name, site_url)

    source = raw_input("What is your directory for posts(content): ")
    source = source or 'content'
    code += "source = '%s'\n" % source
    if not os.path.isdir(source):
        os.makedirs(source)

    output = raw_input("Where is your directory for output(deply): ")
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
    import tempfile
    f = os.path.join(tempfile.gettempdir(), 'liquidluck.json')
    if os.path.exists(f):
        content = open(f).read()
    else:
        import urllib
        content = urllib.urlopen(
            'http://project.lepture.com/liquidluck/themes.json'
        ).read()
        open(f, 'w').write(content)

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
    if not keyword:
        for keyword in themes:
            theme = themes[keyword]
            theme.update({'name': keyword})
            print(SEARCH_TEMPLATE % theme)
        return
    if keyword not in themes:
        print("Can't find theme: %s" % keyword)
        return None
    theme = themes[keyword]
    theme.update({'name': keyword})
    print(SEARCH_TEMPLATE % theme)


def install(keyword):
    themes = __load_themes()
    if keyword not in themes:
        print("can't find theme %s" % keyword)
        return
    theme = themes[keyword]
    repo = theme['git']
    output = '_themes/%s' % keyword
    import subprocess
    subprocess.call(['git', 'clone', repo, output])


def main():
    parser = argparse.ArgumentParser(prog='liquidluck')

    parser.add_argument('command', nargs='?', default='build',
                        help='build | create | search | install | help')
    parser.add_argument('-s', '--settings', default='settings.py',
                        help='setting file')
    parser.add_argument('-t', '--theme', help='theme name')
    parser.add_argument(
        '-v', '--verbose', action='store_true', dest='detail_logging',
        help='show more logging'
    )
    parser.add_argument('--version', action='store_true',
                        help='show version info')

    args = parser.parse_args()

    if args.version:
        print("Felix Felicis Version: %s" % liquidluck.__version__)
        return

    if args.command == 'help':
        launch_help()
        return

    if args.command == 'search':
        search(args.theme)
        return

    if args.command == 'install':
        install(args.theme)
        return

    g.detail_logging = args.detail_logging
    enable_pretty_logging()

    if args.command == 'init' or args.command == 'create':
        create(args.settings)
        return

    if not os.path.exists(args.settings):
        answer = raw_input(
            "Can't find your setting files, "
            "would you like to create one?(Y/n) "
        )
        if answer.lower() == 'n':
            return
        create(args.settings)
        return

    if args.command == 'build':
        generate(args.settings)
        return

if __name__ == '__main__':
    main()
