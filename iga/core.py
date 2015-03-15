"""Core data structures."""

__all__ = [
    'ImmutableOrderedSet',
]

from collections import OrderedDict
from collections import MutableMapping


class ImmutableOrderedSet:
    """An immutable set that remembers the order that elements were
    inserted.
    """

    def __init__(self, iterable):
        self._data = OrderedDict.fromkeys(iterable)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)


class WriteOnceDict(MutableMapping):
    """A dict that does not allow overwriting keys."""

    def __init__(self, iterable=None):
        if iterable:
            self._data = dict(iterable)
        else:
            self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        if key in self._data:
            raise TypeError('cannot overwrite key %r' % key)
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)
