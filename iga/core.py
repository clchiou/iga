"""Core data structures."""

__all__ = [
    'Bimap',
    'ImmutableOrderedSet',
    'WriteOnceBimap',
    'WriteOnceDict',
    'group',
]

from collections import OrderedDict
from collections import MutableMapping
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


class Bimap(MutableMapping):
    """A dict that also allows look up by value."""

    def __init__(self, *, _key_to_value=None, _value_to_key=None):
        self._key_to_value = _key_to_value or {}
        self._value_to_key = _value_to_key or {}

    def inverse(self):
        return Bimap(_key_to_value=dict(self._value_to_key),
                     _value_to_key=dict(self._key_to_value))

    def get_key(self, value, default=None):
        return self._value_to_key.get(value, default)

    def __getitem__(self, key):
        return self._key_to_value[key]

    def __setitem__(self, key, value):
        if value in self._value_to_key:
            raise KeyError('value %r already bound to key %r' %
                           (value, self._value_to_key[value]))
        if key in self._key_to_value:
            del self._value_to_key[self._key_to_value[key]]
        self._key_to_value[key] = value
        self._value_to_key[value] = key

    def __delitem__(self, key):
        value = self._key_to_value[key]
        del self._key_to_value[key]
        del self._value_to_key[value]

    def __iter__(self):
        return iter(self._key_to_value)

    def __len__(self):
        return len(self._key_to_value)

    def __repr__(self):
        return _repr(self, self._key_to_value)

    def __str__(self):
        return _repr(self, self._key_to_value)


class WriteOnceBimap(MutableMapping):

    def __init__(self, *, _bimap=None):
        self._bimap = _bimap or Bimap()

    def inverse(self):
        return WriteOnceBimap(_bimap=self._bimap.inverse())

    def get_key(self, value, default=None):
        return self._bimap.get_key(value, default)

    def __getitem__(self, key):
        return self._bimap[key]

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError('cannot overwrite key %r' % (key,))
        self._bimap[key] = value

    def __delitem__(self, key):
        raise KeyError('cannot delete keys from %s (key=%r)' %
                       (self.__class__.__name__, key))

    def __iter__(self):
        return iter(self._bimap)

    def __len__(self):
        return len(self._bimap)

    def __repr__(self):
        return _repr(self, dict(self._bimap))

    def __str__(self):
        return _repr(self, dict(self._bimap))
