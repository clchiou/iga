"""Package is a collection of build rules indexed by label."""

__all__ = [
    'make_package',
]

from collections import namedtuple

from .core import safe_dict


def make_package(package_name, rules):
    """Make a Package object."""
    # TODO: Check package_name matches rule label.
    return Package(
        package_name=package_name,
        rules=safe_dict((rule.label, rule) for rule in rules),
    )


class Package(namedtuple('Package', 'package_name rules')):
    """Package is a collection of build rules indexed by label."""
    pass
