"""C/C++ build rules."""

__all__ = [
    'CcConfigure',
]

from iga import (
    ConfigureProperty,
    MetaConfigure,
)

from iga import (
    Label,
    Rule,
)


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

    def make_rules(self, package_name):
        """Make Rule objects."""
        # TODO: Actually make rules.
        return []
