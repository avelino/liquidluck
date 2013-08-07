# coding: utf-8
"""
    liquidluck._compat
    ~~~~~~~~~~~~~~~~~~

    Compatible module for python2 and python3.

    :copyright: (c) 2013 by Hsiaoming Yang
"""


import sys
import datetime
PY3 = sys.version_info[0] == 3

if PY3:
    unicode_type = str
    bytes_type = bytes
    text_types = (str,)
else:
    unicode_type = unicode
    bytes_type = str
    text_types = (str, unicode)


def to_unicode(value, encoding='utf-8'):
    """Convert different types of objects to unicode."""
    if isinstance(value, unicode_type):
        return value

    if isinstance(value, bytes_type):
        return unicode_type(value, encoding=encoding)

    if isinstance(value, int):
        return unicode_type(value, encoding=encoding)

    return value


def to_bytes(value, encoding='utf-8'):
    """Convert different types of objects to bytes."""
    if isinstance(value, bytes_type):
        return value
    return value.encode(encoding)


def to_datetime(value):
    """Convert possible value to datetime."""
    if not value:
        return None
    if isinstance(value, datetime.datetime):
        return value
    supported_formats = [
        '%a %b %d %H:%M:%S %Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%dT%H:%M',
        '%Y%m%d %H:%M:%S',
        '%Y%m%d %H:%M',
        '%Y-%m-%d',
        '%Y%m%d',
    ]
    for format in supported_formats:
        try:
            return datetime.datetime.strptime(value, format)
        except ValueError:
            pass
    raise ValueError('Unrecognized date/time: %r' % value)
