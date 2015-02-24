"""Meta-configure object."""

__all__ = [
    'ConfigureProperty',
    'MetaConfigure',
]

import functools
from collections import namedtuple

from .core import IgaError


class MetaConfigure(type):
    """The meta-class of configure classes."""

    def __new__(mcs, cls_name, bases, namespace):
        properties = {
            name: prop for name, prop in namespace.items()
            if isinstance(prop, ConfigureProperty)
        }

        # Sanity check.
        for name in properties:
            if name.startswith('_'):
                raise IgaError(
                    'configure property "%s.%s" starts with "_"' %
                    (cls_name, name))
        for reserved in ('_properties', '_data'):
            if reserved in namespace:
                raise IgaError(
                    'configure property "%s.%s" conflicts with base class' %
                    (cls_name, reserved))

        for name, prop in properties.items():
            namespace[name] = Accessor(name, prop)
            namespace[name].__doc__ = prop.doc
        namespace['_properties'] = properties
        bases = (BaseConfigure,) + bases
        return type.__new__(mcs, cls_name, bases, namespace)


class BaseConfigure:
    """The base class of all configure classes."""

    def __init__(self):
        """Initialize configure object data."""
        self._data = {}
        self._data.update(
            (name, {}) for name, prop in self._properties.items()
            if prop.is_mapping_property()
        )
        self._data.update(
            (name, []) for name, prop in self._properties.items()
            if prop.is_repeated_property()
        )

    def get_accessors(self):
        """Return accessors in a dict."""
        return {name: getattr(self, name) for name in self._properties}

    def has_value(self, name):
        """Test if a property has been set."""
        return name in self._data

    def access_scalar(self, name, scalar_type, args, _):
        """Scalar property accessor."""
        if args:
            value = args[0]
            assert isinstance(value, scalar_type)
            self._data[name] = value
        if name not in self._data:
            raise IgaError('property "%s" has not been set yet' % name)
        return self._data[name]

    def access_mapping(self, name, key_type, value_type, args, _):
        """Mapping property accessor."""
        if not args:
            return self._data[name]
        key = args[0]
        assert isinstance(key, key_type)
        if len(args) > 1:
            value = args[1]
            assert isinstance(value, value_type)
            self._data[name][key] = value
        return self._data[name][key]

    def access_repeated_scalar(self, name, scalar_type, args, _):
        """Repeated scalar property accessor."""
        lst = self._data[name]
        if args:
            assert isinstance(args[0], scalar_type)
            lst.append(args[0])
        return lst

    def access_repeated_tuple(self, name, args, _):
        """Repeated tuple property accessor."""
        lst = self._data[name]
        if args:
            lst.append(tuple(args))
        return lst

    def access_repeated_dict(self, name, _, kwargs):
        """Repeated dict property accessor."""
        lst = self._data[name]
        if kwargs:
            lst.append(kwargs.copy())
        return lst


class ConfigureProperty(namedtuple('ConfigureProperty', 'type doc')):
    """A configure object property."""

    def is_scalar_property(self):
        """True if this is a scalar property."""
        return not (self.is_mapping_property() or self.is_repeated_property())

    def is_mapping_property(self):
        """True if this is a mapping property."""
        return isinstance(self.type, tuple)

    def is_repeated_property(self):
        """True if this is a repeated scalar/tuple/dict property."""
        return isinstance(self.type, list)


class Accessor(namedtuple('Accessor', 'name prop')):
    """A descriptor that wraps a ConfigureProperty object."""

    def __get__(self, configure, _):
        """Return an accessor to the configure object."""
        if self.prop.is_mapping_property():
            accessor = functools.partial(
                configure.access_mapping,
                self.name,
                self.prop.type[0],
                self.prop.type[1])
        elif self.prop.is_repeated_property():
            element_type = self.prop.type[0]
            if element_type is dict:
                accessor = functools.partial(
                    configure.access_repeated_dict,
                    self.name)
            elif element_type is tuple:
                accessor = functools.partial(
                    configure.access_repeated_tuple,
                    self.name)
            else:
                accessor = functools.partial(
                    configure.access_repeated_scalar,
                    self.name,
                    element_type)
        else:
            accessor = functools.partial(
                configure.access_scalar,
                self.name,
                self.prop.type)
        return self._wrap(accessor)

    def _wrap(self, func):
        """Wrap func with a trampoline."""
        def trampoline(*args, **kwargs):
            """A trampoline passing args and kwargs to func."""
            return func(args, kwargs)
        trampoline.__name__ = self.name
        trampoline.__doc__ = self.prop.doc
        return trampoline
