#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from liquidluck.tools import theme
from liquidluck.tools import creator
from liquidluck.tools import webhook
from liquidluck.tools import server
from liquidluck import generator
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings


def main():
    parser = create_parser()
    args = parser.parse_args()
    run_parser(args)


def create_parser():
    parser = argparse.ArgumentParser(prog='liquidluck')

    subparser = parser.add_subparsers(
        title='available commands', dest='subparser'
    )

    parser_create = subparser.add_parser(
        'create', help='create a blog repo',
    )
    parser_create.add_argument(
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

    #: theme support
    parser_search = subparser.add_parser(
        'search', help='search theme'
    )
    parser_search.add_argument('theme', nargs='?', help='theme name')

    parser_install = subparser.add_parser(
        'install', help='install a theme'
    )
    parser_install.add_argument('theme', nargs='?', help='theme name')

    #: utils
    subparser.add_parser(
        'document', help='launch documentation in browser'
    )

    subparser.add_parser(
        'version', help='show Felix Felicis version'
    )

    #: webhook command
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
    parser_webhook.add_argument(
        '-s', '--settings', default='settings.py', help='setting file'
    )

    #: preview server
    parser_server = subparser.add_parser(
        'server', help='start a preview server',
    )
    parser_server.add_argument(
        '-p', '--port', nargs='?', default=8000,
        help='server port'
    )
    parser_server.add_argument(
        '-s', '--settings', default='settings.py', help='setting file'
    )

    return parser


def run_parser(args):
    if args.subparser == 'version':
        import liquidluck
        print("Felix Felicis Version: %s" % liquidluck.__version__)
        return

    if args.subparser == 'document':
        import webbrowser
        webbrowser.open('http://liquidluck.readthedocs.org')
        return

    if args.subparser == 'search':
        theme.search(args.theme)
        return

    if args.subparser == 'install':
        theme.install(args.theme)
        return

    if args.subparser == 'webhook':
        webhook.webhook(args.port, args.daemon, args.settings)
        return

    if args.subparser == 'server':
        generator.load_settings(args.settings)
        if settings.permalink.endswith('.html'):
            permalink = 'html'
        elif settings.permalink.endswith('/'):
            permalink = 'slash'
        else:
            permalink = 'clean'
        server.config(args.port, g.output_directory, permalink)
        server.start_server()
        return

    if args.subparser == 'create':
        creator.create(args.settings)
        return

    if not os.path.exists(args.settings):
        answer = raw_input(
            "Can't find your setting files, "
            "would you like to create one?(Y/n) "
        )
        if answer.lower() == 'n':
            return
        creator.create(args.settings)
        return

    g.detail_logging = args.verbose
    enable_pretty_logging()
    generator.build(args.settings)


if __name__ == '__main__':
    main()
