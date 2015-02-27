"""The iga meta-build system."""

__all__ = [
    # iga.configure
    'ConfigureProperty',
    'MetaConfigure',

    # iga.label
    'Label',

    # iga.rule
    'Rule',
]

# Create "iga.g" module (this should be before other imports).
import iga.tools.namespace
g = iga.tools.namespace.install('g')

from .configure import ConfigureProperty
from .configure import MetaConfigure
from .label import Label
from .rule import Rule
