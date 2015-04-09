"""Convenient methods for checking user inputs."""

__all__ = [
    'check',
    'check_iterable',
    'check_type',
]

from iga.error import IgaError


def check(condition, message, *args):
    if not condition:
        raise IgaError(message % args)


def check_type(var, *types):
    """Check if `var` is of one of the types."""
    check(any(isinstance(var, typ) for typ in types),
          '%r is not one of %r', var, types)


def check_iterable(var, *element_types):
    """Check if `var` is iterable whose elements are of one of the types."""
    check_type(var, tuple, list, set, frozenset)
    for index, element in enumerate(var):
        check(any(isinstance(element, typ) for typ in element_types),
              'lst[%d] == %r is one of %r', index, element, element_types)
