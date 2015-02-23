'''A configure object for an IGA file.'''

__all__ = [
    'IgaConfigure',
]

from iga import ConfigureProperty
from iga import MetaConfigure


class IgaConfigure(metaclass=MetaConfigure):
    '''A configure object for an IGA file.'''

    source_root = ConfigureProperty.data(str, None, '''
    Path to root directory of source code.
    ''')

    build_root = ConfigureProperty.data(str, lambda: 'build', '''
    Path to build output directory.
    ''')

    environment = ConfigureProperty.data(
        (str, dict), lambda: {'default': {}}, '''
    Build environments.
    ''')
