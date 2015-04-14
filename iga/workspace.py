__all__ = [
    'workspace',
]

import logging

import iga.env
import iga.path
from iga.error import IgaError


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def workspace(
        *,
        root=None,
        source='.',
        build='build'):
    """Define workspace variables in root env."""
    root = root or iga.path.get_caller_path(ancestor=1).parent
    LOG.info('root = %s', root)
    if not root.is_dir():
        raise IgaError('"root" is not a dir: %s' % root)
    source = root / source
    LOG.info('source = %s', source)
    if not source.is_dir():
        raise IgaError('"source" is not a dir: %s' % source)
    build = root / build
    LOG.info('build = %s', build)
    iga.env.current().update(
        root=root,
        source=source,
        build=build,
    )
