__version__ = '0.0.0'

__author__ = 'Che-Liang Chiou'
__author_email__ = 'clchiou@gmail.com'
__copyright__ = 'Copyright 2015, Che-Liang Chiou'
__license__ = 'MIT'

__all__ = [
    'workspace',
]


def workspace(**kwargs):
    import iga.context
    iga.context.set_global_context(**kwargs)
