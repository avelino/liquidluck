from liquidluck.options import settings
from liquidluck.util import import_module


def detect_reader(filepath):
    for reader in settings.readers.values():
        reader = import_module(reader)(filepath)
        if reader.support():
            return reader
    return None
