__all__ = [
    'RegistryMixin',
    'reset',
]

import logging
from collections import defaultdict

from iga.core import WriteOnceDict
from iga.error import IgaError


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


_REGISTRY = defaultdict(WriteOnceDict)


def _make_namespace(klass):
    return '%s.%s' % (klass.__module__, klass.__qualname__)


def reset():
    _REGISTRY.clear()


class RegistryMixin:

    @classmethod
    def register(cls, named_obj):
        cls.register_with_name(named_obj.name, named_obj)

    @classmethod
    def register_with_name(cls, name, obj):
        if not isinstance(obj, cls):
            raise IgaError('%r is not of type %r' % (obj, cls))
        namespace = _make_namespace(cls)
        LOG.info('add object named %r to %s', name, namespace)
        _REGISTRY[namespace][name] = obj

    @classmethod
    def get_all_objects(cls):
        namespace = _make_namespace(cls)
        return _REGISTRY[namespace]

    @classmethod
    def get_object(cls, name):
        return cls.get_all_objects()[name]
