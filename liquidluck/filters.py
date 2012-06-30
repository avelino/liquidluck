#!/usr/bin/env python
# -*- coding: utf-8 -*-


def xmldatetime(value):
    """ this is a jinja filter """
    from liquidluck.options import settings
    timezone = '+00:00'
    if isinstance(settings.timezone, int):
        zone = abs(settings.timezone)
        if zone > 9:
            timezone = '%s:00' % zone
        else:
            timezone = '0%s:00' % zone

        if settings.timezone < 0:
            timezone = '-%s' % timezone
        else:
            timezone = '+%s' % timezone
    elif isinstance(settings.timezone, str):
        timezone = settings.timezone

    value = value.strftime('%Y-%m-%dT%H:%M:%S')
    return '%s%s' % (value, timezone)
