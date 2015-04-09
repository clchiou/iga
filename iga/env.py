__all__ = [
    'current',
    'enter_child_env',
    'root',

    # Global registry.
    'register',
    'find',
]

import contextlib
import logging
from collections import ChainMap

from iga.core import WriteOnceDict


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


_ROOT = ChainMap(WriteOnceDict())


def current():
    """Return the current env object."""
    return current.current


current.current = _ROOT


@contextlib.contextmanager
def enter_child_env():
    """Enter a child env context."""
    child = current.current.new_child(WriteOnceDict())
    current.current, parent = child, current.current
    yield child
    current.current = parent


def root():
    """Return the singleton root env object."""
    return _ROOT


def register(entity):
    LOG.info('add %s %r', entity.kind, entity.name)
    if entity.kind not in root():
        root()[entity.kind] = WriteOnceDict()
    root()[entity.kind][entity.name] = entity


def find(kind, name):
    return root()[kind][name]
