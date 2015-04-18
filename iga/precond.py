"""Convenient methods for checking user inputs."""

__all__ = [
    'check',
    'check_type',
]

from iga.error import IgaError


def check(condition, message, *args):
    if not condition:
        raise IgaError(message % args)


def check_type(var, *types):
    """Check if `var` is of one of the types."""
    check(all(isinstance(var, typ) for typ in types),
          '%r is not one of %r', var, types)
