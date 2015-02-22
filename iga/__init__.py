'''The iga meta-build system.'''

__all__ = [
    'DEFAULT_VARIANT',
    'Error',
]


DEFAULT_VARIANT = 'default'


class Error(Exception):
    '''An error inside iga.'''
    pass
