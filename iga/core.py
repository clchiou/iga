"""Core data structures."""

__all__ = [
    'ImmutableOrderedSet',
    'OrderedSet',
    'KeyedSets',
    'WriteOnceDict',
    'group',
    'list_difference',
]

from collections import OrderedDict
from collections import MutableMapping
from collections import MutableSet
from collections import Set
from collections import defaultdict


def group(items, key=None, as_dict=True):
    """Group items by applying key function."""
    key = key or (lambda item: item)
    groups = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    if as_dict:
        groups = dict(groups)
    return groups


def list_difference(this, other):
    """Return elements in this list but not in the other."""
    other = frozenset(other)
    return [element for element in this if element not in other]


def _repr(obj, data):
    return '%s(%r)' % (obj.__class__.__name__, data)


class ImmutableOrderedSet(Set):
    """An immutable set that remembers the order that elements were
    inserted.
    """

    def __init__(self, iterable):
        self._data = OrderedDict.fromkeys(iterable)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return _repr(self, list(self._data.keys()))

    def __str__(self):
        return _repr(self, list(self._data.keys()))


class OrderedSet(MutableSet, ImmutableOrderedSet):
    """A set that remembers the order that elements were inserted."""

    def __init__(self, iterable=()):
        super().__init__(iterable)

    def add(self, value):
        self._data[value] = None

    def discard(self, value):
        self._data.pop(value, None)


class WriteOnceDict(MutableMapping):
    """A dict that does not allow overwriting keys."""

    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        if key in self._data:
            raise KeyError('cannot overwrite key %r' % (key,))
        self._data[key] = value

    def __delitem__(self, key):
        raise KeyError('cannot delete keys from %s (key=%r)' %
                       (self.__class__.__name__, key))

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return _repr(self, self._data)

    def __str__(self):
        return _repr(self, self._data)


class KeyedSets:
    """A collection of sets indexed by predefined keys."""

    def __init__(self, keys, set_type=OrderedSet):
        self._sets = {key: set_type() for key in keys}

    def __bool__(self):
        return any(self._sets.values())

    def __contains__(self, key):
        return key in self._sets

    def __iter__(self):
        return iter(self._sets)

    def __getitem__(self, key):
        return self._sets[key]

    def __ior__(self, other):
        for key in other:
            if key in self._sets:
                self._sets[key] |= other[key]
        return self

    def keys(self):
        return self._sets.keys()

    def as_dict_of_sets(self):
        return dict((key, set(kset)) for key, kset in self._sets.items())
