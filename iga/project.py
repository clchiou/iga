"""Define a project."""

__all__ = [
    'project',
]

import logging
import os.path
import sys

import iga.context
import iga.main
import iga.path
from iga.error import IgaError


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def project(
        *,
        project_root=None,
        source='.',
        build='build',
        variables=None):
    """Define a project."""
    if project_root is None:
        project_root = iga.path.get_caller_path(ancestor=1)
        if project_root is None:
            raise IgaError('cannot determine project_root')
        project_root = os.path.dirname(project_root)
    LOG.info('project_root = %r', project_root)
    source = os.path.normpath(os.path.join(project_root, source))
    LOG.info('source = %r', source)
    build = os.path.normpath(os.path.join(project_root, build))
    LOG.info('build = %r', build)
    variables = variables or {}
    iga.context.get_context().update(
        project_root=project_root,
        source=source,
        build=build,
        variables=variables,
    )
    sys.exit(iga.main.main(sys.argv))
