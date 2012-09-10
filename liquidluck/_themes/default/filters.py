#!/usr/bin/env python


def description(key):
    from liquidluck.options import settings
    dct = settings.theme['vars'].get('descriptions')
    if not isinstance(dct, dict):
        return ''
    if key not in dct:
        return ''
    return dct[key]
