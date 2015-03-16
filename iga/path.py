"""File path utilities."""

__all__ = [
    'get_caller_path',
    'to_relpath',
]

import inspect
import os
import os.path

import iga.context


def get_caller_path(ancestor):
    """Return the file path of i-th ancestor of the caller, or None if
    inspection is not supported or out of call stack range.

    The zero-th ancestor is the caller, first ancestor is caller's
    caller, and so on.
    """
    call_stack = inspect.stack(context=0)
    if call_stack is None:
        return None
    index = 1 + ancestor
    if index >= len(call_stack):
        return None
    return os.path.join(os.getcwd(), call_stack[index][1])


def to_relpath(string, *, context=None):
    context = context or iga.context.get_context()
    path = string if os.sep == '/' else string.replace('/', os.sep)
    path = os.path.join(context['source'], path)
    return os.path.relpath(path, context['project_root'])
