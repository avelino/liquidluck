#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import liquidluck
from liquidluck.generator import build
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g


def launch_help():
    import webbrowser
    webbrowser.open('http://liquidluck.readthedocs.org')


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

    #: theme support
    subparser.add_parser(
        'search', help='search theme'
    ).add_argument('theme', nargs='?', help='theme name')

    subparser.add_parser(
        'install', help='install a theme'
    ).add_argument('theme', nargs='?', help='theme name')

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

    args = parser.parse_args()

    if args.subparser == 'version':
        print("Felix Felicis Version: %s" % liquidluck.__version__)
        return

    if args.subparser == 'document':
        launch_help()
        return

    if args.subparser == 'search':
        from liquidluck.tools.theme import search
        search(args.theme)
        return

    if args.subparser == 'install':
        from liquidluck.tools.theme import install
        install(args.theme)
        return

    if args.subparser == 'create':
        from liquidluck.tools.creator import create
        create(args.settings)
        return

    if args.subparser == 'webhook':
        from liquidluck.tools.webhook import webhook
        webhook(args.port, args.daemon, args.settings)
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
