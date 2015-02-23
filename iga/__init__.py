'''The iga meta-build system.'''

__all__ = [
    'g',

    # iga.configure
    'ConfigureProperty',
    'MetaConfigure',

    # iga.context
    'make_default_context',

    # iga.core
    'IgaError',

    # iga.label
    'Label',
]

# Create "iga.g" module (this should be before other imports).
from . import namespace
g = namespace.install('g')

from .configure import ConfigureProperty
from .configure import MetaConfigure
from .context import make_default_context
from .core import IgaError
from .label import Label
