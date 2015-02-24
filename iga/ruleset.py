"""RuleSet object for making rules."""

__all__ = [
    'RuleSet',
]

from collections import namedtuple


class RuleSet(namedtuple('RuleSet', 'make_configure make_rules')):
    """RuleSet object for making rules."""
    pass
