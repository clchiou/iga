"""The labels provide a namespace of files and modules in a platform-
independent manner (like path separator is always '/').
"""

__all__ = [
    'FileLabel',
    'ModuleLabel',
]

import posixpath
from collections import namedtuple

import iga.context
import iga.path
from iga.error import IgaError


class Label(namedtuple('Label', 'package target')):

    def __str__(self):
        return '//%s:%s' % (self.package, self.target)

    def __repr__(self):
        return ('%s(\'//%s:%s\')' %
                (self.__class__.__name__, self.package, self.target))


class FileLabel(Label):
    """The labels that refer to a file."""

    @staticmethod
    def copy(label):
        """Create a copy of label."""
        return FileLabel(package=label.package, target=label.target)

    @staticmethod
    def expand(label_string, *, package=None):
        if package is None:
            package = iga.context.get_context()['package']
        # TODO: Support glob for local and generated files (labels).
        label = _parse_label(FileLabel, label_string, package)
        return [label]

    def replace(self, *, basename=None, ext=None):
        """Replace a part of the label."""
        if basename is not None:
            top, bottom = posixpath.split(self.target)
            if callable(basename):
                bottom = basename(bottom)
            else:
                bottom = basename
            target = posixpath.join(top, bottom)
            return FileLabel(package=self.package, target=target)
        if ext is not None:
            top, bottom = posixpath.splitext(self.target)
            if callable(ext):
                bottom = ext(bottom)
            else:
                bottom = ext
            target = top + bottom
            return FileLabel(package=self.package, target=target)
        return self

    @property
    def relpath(self):
        """Return the relative path of the file."""
        # FIXME: Call to_source_relpath here is incorrect!
        return iga.path.to_source_relpath(
            posixpath.join(self.package, self.target))


class ModuleLabel(Label):
    """The labels that refer to a module."""

    @staticmethod
    def parse(label_string, *, package=None):
        """Parse ModuleLabel string representation."""
        if package is None:
            package = iga.context.get_context()['package']
        return _parse_label(ModuleLabel, label_string, package)


def parse_label(label_string):
    return _parse_label(Label, label_string, None)


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
