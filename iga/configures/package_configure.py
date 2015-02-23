'''A configure object for a PACKAGE file.'''

__all__ = [
    'PackageConfigure',
]

from iga import ConfigureProperty
from iga import MetaConfigure


class PackageConfigure(metaclass=MetaConfigure):
    '''A configure object for a PACKAGE file.'''

    def __init__(self):
        self.rules = []

    def add_rule(self, property_name, kwargs):
        '''Add a build rule to this package.'''
        self.rules.append((kwargs['name'], property_name))

    c_binary = ConfigureProperty.func(add_rule, '''
    Rule of C executable.
    ''')

    c_library = ConfigureProperty.func(add_rule, '''
    Rule of C library.
    ''')
