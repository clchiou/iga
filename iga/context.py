"""Global contexts.

It is unfortunate that some functions require a context when they are
called.  I choose to implement this context as a global, chained list of
dict-like objects.  The alternative is to make all call sites passing in
a context, which makes call sites complicated and sometimes impossible.
"""

__all__ = [
    'current',
    'create',
]

import contextlib
from collections import ChainMap

from iga.core import WriteOnceDict


def current():
    """Return the current environment object."""
    return current.current


# Root context.
current.current = ChainMap(WriteOnceDict())


@contextlib.contextmanager
def create():
    """Create and enter a child context."""
    child = current.current.new_child(WriteOnceDict())
    current.current, parent = child, current.current
    yield child
    current.current = parent
