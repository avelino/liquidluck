#!/usr/bin/env python
import os
import sys
import liquidluck
from liquidluck.tools import theme
from liquidluck.tools import creator
from liquidluck.tools import webhook
from liquidluck.tools import server
from liquidluck import generator
from liquidluck.options import enable_pretty_logging
from liquidluck.options import g, settings
from docopt import docopt

documentation = {}
documentation['help'] = """Felix Felicis %(version)s

Usage:
    liquidluck create [-s <file>|--settings=<file>]
    liquidluck build [-s <file>|--settings=<file>] [-v|--verbose]
    liquidluck server [-s <file>|--settings=<file>] [-p <port>|--port=<port>]
    liquidluck search [<theme>] [-c|--clean] [-f|--force]
    liquidluck install <theme>
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
    --version               show version.
""" % {
    'version': liquidluck.__version__,
    'webhook': '[-s <file>|--settings=<file>] [-p <port>|--port=<port>]'
}

documentation['create'] = """
Usage:
    liquidluck create [-s <file>|--settings=<file>]

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
    liquidluck install <theme>

Options:
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
    enable_pretty_logging()
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

    if command == 'create':
        creator.create(args['--settings'] or 'settings.py')
    elif command == 'build':
        arg_settings = args['--settings'] or 'settings.py'
        if not os.path.exists(arg_settings):
            answer = raw_input(
                "Can't find your setting files, "
                "would you like to create one?(Y/n) "
            )
            if answer.lower() == 'n':
                return
            creator.create(arg_settings)
        else:
            g.detail_logging = args['--verbose']
            generator.build(arg_settings)
    elif command == 'server':
        arg_settings = args['--settings'] or 'settings.py'
        arg_port = int(args['--port'] or 8000)
        if not os.path.exists(arg_settings):
            print('setting file not found')
            server.config(arg_port)
            server.start_server()
        else:
            generator.load_settings(arg_settings)
        if settings.permalink.endswith('.html'):
            permalink = 'html'
        elif settings.permalink.endswith('/'):
            permalink = 'slash'
        else:
            permalink = 'clean'
        server.config(arg_port, g.output_directory, permalink)
        server.start_server()
    elif command == 'search':
        arg_theme = args['<theme>'] or None
        arg_clean = args['--clean']
        arg_force = args['--force']
        theme.search(arg_theme, arg_clean, arg_force)
    elif command == 'install':
        arg_theme = args['<theme>'] or None
        theme.install(arg_theme)
    elif command == 'webhook':
        arg_settings = args['--settings'] or 'settings.py'
        arg_port = int(args['--port'] or 9000)
        action = (args['start'] and 'start') or (args['stop'] and 'stop') \
                or (args['restart'] and 'restart')
        webhook.webhook(arg_port, action, arg_settings)


if __name__ == '__main__':
    main()
