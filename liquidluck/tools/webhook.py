import sys
import os
import time
import atexit
import signal
import subprocess
from wsgiref.simple_server import make_server


CWDPATH = os.path.abspath('.')
SETTINGS = 'settings.py'
PORT = 8000


def _call(cmd):
    subprocess.call(cmd.split(), cwd=CWDPATH)


def _update():
    if os.path.isdir(os.path.join(CWDPATH, '.git')):
        _call('git pull')
        if os.path.exists(os.path.join(CWDPATH, '.gitmodules')):
            _call('git submodule init')
            _call('git submodule update')
        return

    if os.path.isdir(os.path.join(CWDPATH, '.hg')):
        _call('hg pull')
        return


def app(environ, start_response):
    path = environ['PATH_INFO']
    start_response('200 OK', [('Content-type', 'text/plain')])
    if path == '/webhook':
        _update()
        _call('liquidluck build -s %s' % SETTINGS)
    yield 'Ok'


class Daemon(object):
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.
    """

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = (
                "pidfile {0} already exist. "
                "Daemon already running?\n"
            )
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = (
                "pidfile {0} does not exist. "
                "Daemon not running?\n"
            )
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print(e)
                    sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""


class ServerDaemon(Daemon):
    def run(self):
        global PORT
        make_server('', PORT, app).serve_forever()


def webhook(port, command='start', settings='settings.py'):
    global PORT
    global SETTINGS
    PORT = int(port)
    SETTINGS = settings
    d = ServerDaemon('/tmp/liquidluck.pid')
    if command == 'start':
        d.start()
    elif command == 'stop':
        d.stop()
    elif command == 'restart':
        d.restart()
    else:
        print("Invalid Command")
