#!/usr/bin/env python
# -*- coding: utf-8 -*-


def xmldatetime(value):
    """ this is a jinja filter """
    import datetime
    if not isinstance(value, datetime.datetime):
        return value
    from liquidluck.options import settings
    value = value.strftime('%Y-%m-%dT%H:%M:%S')
    return '%s%s' % (value, settings.timezone)
