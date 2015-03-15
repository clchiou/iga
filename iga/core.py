"""Core data structures."""

__all__ = [
    'ImmutableOrderedSet',
]

from collections import OrderedDict


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
