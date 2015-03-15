"""The labels provide a namespace of files and modules in a platform-
independent manner (like path separator is always '/').
"""

__all__ = [
    'ModuleLabel',
]

from collections import namedtuple

import iga.path
from iga.error import IgaError


Label = namedtuple('Label', 'package target')


class ModuleLabel(Label):
    """The labels that refer to a module."""

    @staticmethod
    def parse(label_string, *, package=None):
        """Parse ModuleLabel string representation."""
        if package is None:
            package = iga.path.get_caller_path(ancestor=1)
            if package is None:
                raise IgaError('cannot determine package path')
            package = iga.path.get_package(package)
        return _parse_label(ModuleLabel, label_string, package)


def _parse_label(cls, label_string, package_from_context):
    """Parse label string representation."""
    if label_string.startswith('//'):
        package_start = 2
        package_end = (_find_or_none(label_string, ':', package_start) or
                       len(label_string))
        package = label_string[package_start:package_end]
        if not package:
            raise IgaError('empty package of %r' % label_string)
    else:
        package_start = package_end = 0
        package = None

    if label_string[package_end:package_end+1] == ':':
        target_start = package_end + 1
    else:
        target_start = package_end
    target = label_string[target_start:]

    if not package and not target:
        raise IgaError('cannot parse %r' % label_string)
    package = package or package_from_context
    if not package:
        raise IgaError('cannot parse package part from %r' % label_string)
    target = target or _default_target(package)
    if not target:
        raise IgaError('cannot parse target part from %r' % label_string)

    return cls(package=package, target=target)


def _find_or_none(string, substring, start):
    """Find the start of the substring or return None."""
    index = string.find(substring, start)
    return index if index != -1 else None


def _default_target(package):
    """Return the default target from a package string."""
    return package[package.rfind('/')+1:]
