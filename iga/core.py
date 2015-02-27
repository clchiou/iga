"""Core utilities."""

__all__ = [
    'IgaError',
    'as_dict',
    'safe_dict',
    'safe_update',
]


class IgaError(Exception):
    """An iga internal error."""
    pass


def as_dict(**kwargs):
    """Make you write less quote marks for a dict."""
    return kwargs.copy()


def safe_dict(pairs):
    """Check duplicated keys when creating a dict."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise KeyError('duplicated key \'%s\'' % key)
        result[key] = value
    return result


def safe_update(target, source):
    """Check duplicated keys when updating a dict."""
    if hasattr(source, 'keys'):
        pairs = ((key, source[key]) for key in source)
    else:
        pairs = source
    for key, value in pairs:
        if key in target:
            raise KeyError('duplicated key \'%s\'' % key)
        target[key] = value
    return target
