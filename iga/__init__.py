"""The iga meta-build system."""

__all__ = [
    # iga.configure
    'ConfigureProperty',
    'MetaConfigure',
]

# Create "iga.g" module (this should be before other imports).
from iga.utilities import namespace
g = namespace.install('g')

from .configure import ConfigureProperty
from .configure import MetaConfigure
