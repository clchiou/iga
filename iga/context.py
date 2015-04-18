"""Global contexts.

It is unfortunate that some functions require a context when they are
called.  I choose to implement this context as a global, chained list of
dict-like objects.  The alternative is to make all call sites passing in
a context, which makes call sites complicated and sometimes impossible.
"""

__all__ = [
    'current',
    'create',
    'load_workspace',
    'set_global_context',
]

import contextlib
import logging
from collections import ChainMap
from pathlib import Path

from iga.core import WriteOnceDict
from iga.error import IgaError


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


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


def set_global_context(
        *,
        source='.',
        build='build',
        variables=None):
    root = current()['root']
    source = root / source
    LOG.info('source = %s', source)
    if not source.is_dir():
        raise IgaError('%s is not a dir' % source)
    build = root / build
    LOG.info('build = %s', build)
    variables = variables or {}
    current().update(
        source=source,
        build=build,
        variables=variables,
    )


def load_workspace(workspace_path=None):
    workspace_path = workspace_path or Path.cwd() / 'workspace.py'

    root = workspace_path.parent.resolve()
    LOG.info('root = %s', root)
    if not root.is_dir():
        raise IgaError('%s is not a dir' % root)
    current()['root'] = root

    LOG.info('load %s', workspace_path)
    with workspace_path.open('r') as workspace_file:
        code = workspace_file.read()
    code = compile(code, str(workspace_path), 'exec')
    exec(code, {})
