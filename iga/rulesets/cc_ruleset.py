"""C/C++ rule set."""

__all__ = [
    'make_cc_ruleset',
]

from iga.configure import ConfigureProperty
from iga.configure import MetaConfigure
from iga.ruleset import RuleSet


def make_cc_ruleset():
    """Make a default CcRuleset object."""
    return RuleSet(make_configure=CcConfigure, make_rules=make_cc_rules)


class CcConfigure(metaclass=MetaConfigure):
    """C/C++ build rules."""

    c_binary = ConfigureProperty(
        [dict], """Build rule for C executable.""")

    c_library = ConfigureProperty(
        [dict], """Build rule for C library.""")

    cc_binary = ConfigureProperty(
        [dict], """Build rule for C++ executable.""")

    cc_library = ConfigureProperty(
        [dict], """Build rule for C++ library.""")


def make_cc_rules(package, configure):
    """Make Rule objects from a CcConfigure object."""
    pass
