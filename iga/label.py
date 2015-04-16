"""Implement Blaze/Bazel label."""

__all__ = [
    'Label',
]

from collections import namedtuple
from pathlib import PurePath
from pathlib import PurePosixPath

import iga.env
import iga.fargparse
from iga.error import IgaError


class Label(namedtuple('Label', 'package target')):

    @staticmethod
    def parse(label_string, current_package):
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
        package = package or current_package
        if not package:
            raise IgaError('cannot parse package part from %r' % label_string)
        target = target or _default_target(package)
        if not target:
            raise IgaError('cannot parse target part from %r' % label_string)

        return Label(
            package=PurePosixPath(package),
            target=PurePosixPath(target),
        )

    @staticmethod
    def parse_cmdline(label_string):
        """Parse label string from command-line."""
        if not label_string.startswith('//'):
            label_string = '//' + label_string
        return Label.parse(label_string, None)

    @staticmethod
    def parse_buildfile(label_string):
        """Parse label string within BUILD file evaluation environment."""
        if not isinstance(label_string, str):
            raise iga.fargparse.ParseError()
        return Label.parse(label_string, iga.env.current()['package'])

    @staticmethod
    def make(package, target):
        if not isinstance(package, PurePath):
            package = PurePosixPath(package)
        if not isinstance(target, PurePath):
            target = PurePosixPath(target)
        return Label(package=package, target=target)

    def __str__(self):
        return '//%s:%s' % (self.package, self.target)

    @property
    def name(self):
        return self.target.name

    def with_name(self, name):
        return Label(self.package, self.target.with_name(name))


iga.fargparse.Parser.register_parse_func(Label, Label.parse_buildfile)


def _find_or_none(string, substring, start):
    """Find the start of the substring or return None."""
    index = string.find(substring, start)
    return index if index != -1 else None


def _default_target(package):
    """Return the default target from a package string."""
    return package[package.rfind('/')+1:]
