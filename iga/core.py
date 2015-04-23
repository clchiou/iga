"""Core data structures."""

__all__ = [
    'ImmutableOrderedSet',
    'OrderedSet',
    'KeyedSets',
    'WriteOnceDict',
    'group',
    'traverse',
]

from collections import OrderedDict
from collections import Mapping
from collections import MutableMapping
from collections import MutableSet
from collections import Set
from collections import defaultdict


def group(items, key=None, as_dict=True):
    """Group items by applying key function.

    Return a `defaultdict(list)` object if as_dict is False.
    """
    key = key or (lambda item: item)
    groups = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    if as_dict:
        groups = dict(groups)
    return groups


def traverse(node, expand):
    yield node
    for more_node in expand(node):
        yield from traverse(more_node, expand)


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

    def update(self, other):
        for value in other:
            self.add(value)

    def difference_update(self, other):
        if other is self:
            self.clear()
            return
        for value in other:
            self.discard(value)


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


class KeyedSets(Mapping):
    """A collection of sets indexed by predefined keys."""

    def __init__(self, keys, *, set_like=OrderedSet):
        self._sets = {key: set_like() for key in keys}

    def __bool__(self):
        return any(self._sets.values())

    def __len__(self):
        return len(self._sets)

    def __iter__(self):
        return iter(self._sets)

    def __contains__(self, key):
        return key in self._sets

    def __getitem__(self, key):
        return self._sets[key]

    def update(self, other):
        for key in other:
            if key in self._sets:
                self._sets[key].update(other[key])

    def difference_update(self, other):
        for key in other:
            if key in self._sets:
                self._sets[key].difference_update(other[key])

    def all_values(self):
        for key in sorted(self):
            yield from self[key]

    def as_dict_of_sets(self):
        return dict((key, set(kset)) for key, kset in self._sets.items())
