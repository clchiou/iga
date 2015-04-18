__version__ = '0.0.0-dev'

__all__ = [
    'workspace',
]


def workspace(**kwargs):
    import iga.context
    iga.context.set_global_context(**kwargs)
