'''Meta-configure object.'''

__all__ = [
    'ConfigureProperty',
    'MetaConfigure',
]

import functools
from collections import namedtuple

from .core import IgaError


class MetaConfigure(type):
    '''The meta-class of configure classes.'''

    def __new__(mcs, name, bases, namespace):
        properties = {
            name: prop for name, prop in namespace.items()
            if isinstance(prop, ConfigureProperty)
        }
        if any(name.startswith('_') for name in properties):
            raise IgaError('configure property starts with "_"')
        cls_namespace = {
            '__init__': functools.partialmethod(
                MetaConfigure.init, namespace.get('__init__')),
            '_accessors_as_dict': MetaConfigure.accessors_as_dict,
            '_properties': properties,
        }
        cls_namespace.update(
            (name, prop.as_accessor(name)) for name, prop in properties.items()
        )
        return type.__new__(mcs, name, bases, cls_namespace)

    def init(self, chained_init, *args, **kwargs):
        '''Initialize a configure object.'''
        self._data = {
            name: prop.default() for name, prop in self._properties.items()
            if prop.default is not None
        }
        if chained_init is not None:
            chained_init(self, *args, **kwargs)

    def accessors_as_dict(self):
        '''Return accessors in a dict.'''
        return {name: getattr(self, name) for name in self._properties}


class ConfigureProperty(
        namedtuple('ConfigureProperty', 'type default function description')):
    '''A configure object property.'''

    FunctionType = 'FunctionType'

    @staticmethod
    def data(type, default, description):
        '''Make a data property.'''
        return ConfigureProperty(
            type=type,
            default=default,
            function=None,
            description=description,
        )

    @staticmethod
    def func(function, description):
        '''Make a function property.'''
        return ConfigureProperty(
            type=ConfigureProperty.FunctionType,
            default=None,
            function=function,
            description=description,
        )

    def as_accessor(self, name):
        '''Make an accessor function of this property.'''
        if self.type == ConfigureProperty.FunctionType:
            make = self._make_function_accessor
        elif isinstance(self.type, tuple):
            make = self._make_mapping_accessor
        else:
            make = self._make_scalar_accessor
        accessor = make(name)
        accessor.__doc__ = self.description
        return accessor

    def _make_function_accessor(prop, name):
        '''Make a function property accessor.'''
        def function_accessor(self, **kwargs):
            '''An accessor of a function property.'''
            return prop.function(self, name, kwargs)
        return function_accessor

    def _make_scalar_accessor(prop, name):
        '''Make a scalar property accessor.'''
        def scalar_accessor(self, *args):
            '''An accessor of a scalar property.'''
            if args:
                assert isinstance(args[0], prop.type)
                self._data[name] = args[0]
            try:
                return self._data[name]
            except KeyError:
                raise IgaError('property "%s" has not been set yet' % name)
        return scalar_accessor

    def _make_mapping_accessor(prop, name):
        '''Make a mapping property accessor.'''
        def mapping_accessor(self, key, *args):
            '''An accessor of a mapping property.'''
            assert isinstance(key, prop.type[0])
            if args:
                assert isinstance(args[0], prop.type[1])
                self._data[name][key] = args[0]
            return self._data[name][key]
        return mapping_accessor
