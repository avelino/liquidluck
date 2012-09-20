#!/usr/bin/env python
import os
import sys
import liquidluck
from liquidluck.tools import theme
from liquidluck.tools import webhook
from liquidluck.tools import server
from liquidluck import generator
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings
from docopt import docopt

documentation = {}
documentation['help'] = """Felix Felicis %(version)s

Usage:
    liquidluck init [-s <file>|--settings=<file>]
    liquidluck build [-s <file>|--settings=<file>] [-v|--verbose]
    liquidluck server [-s <file>|--settings=<file>] [-p <port>|--port=<port>]
    liquidluck search [<theme>] [-c|--clean] [-f|--force]
    liquidluck install <theme> [-g|--global]
    liquidluck webhook (start|stop|restart) %(webhook)s
    liquidluck -h | --help
    liquidluck --version

Options:
    -h --help               show this screen.
    -v --verbose            show more log.
    -s --settings=<file>    specify a setting file.
    -p --port=<port>        specify the server port.
    -f --force              search a theme without cache
    -c --clean              show theme name only.
    -g --global             install theme to global theme folder.
    --version               show version.
""" % {
    'version': liquidluck.__version__,
    'webhook': '[-s <file>|--settings=<file>] [-p <port>|--port=<port>]'
}

documentation['init'] = """
Usage:
    liquidluck init [-s <file>|--settings=<file>]

Options:
    -h --help               show this screen.
    -s --settings=<file>    specify a setting file.
"""

documentation['build'] = """
Usage:
    liquidluck build [-s <file>|--settings=<file>] [-v|--verbose]

Options:
    -h --help               show this screen.
    -v --verbose            show more log.
    -s --settings=<file>    specify a setting file.
"""

documentation['server'] = """
Usage:
    liquidluck server [-s <file>|--settings=<file>] [-p <port>|--port=<port>]

Options:
    -h --help               show this screen.
    -s --settings=<file>    specify a setting file.
    -p --port=<port>        specify the server port.
"""

documentation['search'] = """
Usage:
    liquidluck search [<theme>] [-c|--clean] [-f|--force]

Options:
    -h --help               show this screen.
    -c --clean              show theme name only.
    -f --force              search a theme without cache
"""

documentation['install'] = """
Usage:
    liquidluck install <theme> [-g|--global]

Options:
    -g --global             install theme to global theme folder.
    -h --help               show this screen.
"""

documentation['webhook'] = """
Usage:
    liquidluck webhook (start|stop|restart) %s

Options:
    -h --help               show this screen.
    -s --settings=<file>    specify a setting file.
    -p --port=<port>        specify the server port.
""" % '[-s <file>|--settings=<file>] [-p <port>|--port=<port>]'


def main():
    command = 'help'
    if len(sys.argv) > 1:
        command = sys.argv[1]

    if command in documentation:
        args = docopt(documentation[command])
    else:
        args = docopt(
            documentation['help'],
            version='Felix Felicis v%s' % liquidluck.__version__
        )

    arg_settings = args.get('--settings') or generator.find_settings()
    arg_verbose = args.get('--verbose')
    if arg_verbose:
        enable_pretty_logging('debug')
    else:
        enable_pretty_logging('info')
    arg_port = args.get('--port') or '8000'

    arg_theme = args.get('<theme>') or None
    arg_clean = args.get('--clean')
    arg_force = args.get('--force')
    arg_global = args.get('--global')

    if command == 'init':
        generator.create_settings(arg_settings)
    elif command == 'build':
        if not arg_settings:
            answer = raw_input(
                "Can't find your setting files, "
                "would you like to create one?(Y/n) "
            )
            if answer.lower() == 'n':
                return
            generator.create_settings(arg_settings)
        else:
            generator.build(arg_settings)
    elif command == 'server':
        if arg_settings and os.path.exists(arg_settings):
            generator.load_settings(arg_settings)
        else:
            print('setting file not found')
            server.config(arg_port)
            server.start_server()

        permalink = settings.config.get('permalink')
        if permalink.endswith('.html'):
            _type = 'html'
        elif permalink.endswith('/'):
            _type = 'slash'
        else:
            _type = 'clean'
        server.config(arg_port, g.output_directory, _type)
        server.start_server()
    elif command == 'search':
        theme.search(arg_theme, arg_clean, arg_force)
    elif command == 'install':
        theme.install(arg_theme, arg_global)
    elif command == 'webhook':
        action = (args['start'] and 'start') or (args['stop'] and 'stop') \
                or (args['restart'] and 'restart')
        webhook.webhook(arg_port, action, arg_settings)


if __name__ == '__main__':
    main()
