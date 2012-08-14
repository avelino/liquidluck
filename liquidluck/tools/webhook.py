import sys
import os
import time
import atexit
import subprocess
from signal import SIGTERM
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
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null',
                 stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror)
            )
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid and self.check_pid_exists(pid):
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized by
        start() or restart().
        """

    def check_pid_exists(self, pid):
        """
        Check a PID is exists or already quit.
        This will be called when first init of this class to avoid some
        fake PID file
        """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True


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
