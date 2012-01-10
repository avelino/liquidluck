import sys
import datetime
from .namespace import ns


class Logger(object):
    DEBUG = "\033[35m"
    INFO = "\033[32m"
    WARN = "\033[33m"
    ERROR = "\033[31m"
    TEXT = "\033[37m"
    ENDC = "\033[0m"

    @classmethod
    def _deco(cls, msg, color):
        return '%s%s%s' % (color, msg, cls.ENDC)

    @classmethod
    def _echo(cls, msg, color):
        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        return '%s %s' % (cls._deco(now, color), cls._deco(msg, cls.TEXT))

    @classmethod
    def _stdout(cls, msg):
        sys.stdout.write('%s\n' % msg)
        sys.stdout.flush()

    @classmethod
    def _stderr(cls, msg):
        sys.stderr.write('%s\n' % msg)
        sys.stderr.flush()

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def debug(self, msg):
        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self._stdout(self._deco('%s %s' % (now, msg), self.DEBUG))

    def info(self, msg):
        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self._stdout('%s %s' % (
            self._deco(now, self.INFO), self._deco(msg, self.TEXT)
        ))

    def warn(self, msg):
        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self._stdout(self._deco('%s %s' % (now, msg), self.WARN))

    def error(self, msg):
        now = datetime.datetime.now().strftime(' %H:%M:%S ')
        self._stderr(self._deco('%s %s' % (now, msg), self.ERROR))


_logger = Logger.instance()
if hasattr(ns, 'disable_log') and ns.disable_log:
    info = lambda o: o
else:
    info = _logger.info
debug = _logger.debug
warn = _logger.warn
error = _logger.error
