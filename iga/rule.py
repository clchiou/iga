"""Build rule object."""

__all__ = [
    'Rule',
]

from collections import namedtuple


class Rule(namedtuple('Rule', 'label')):
    """Rule object representing a build rule."""
    pass
