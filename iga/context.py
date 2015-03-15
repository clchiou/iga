"""Execution context."""

__all__ = [
    'get_context',
]

from iga.core import WriteOnceDict


_CONTEXT = WriteOnceDict()


def get_context():
    """Return the execution context."""
    return _CONTEXT
