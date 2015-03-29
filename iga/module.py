__all__ = [
    'add_module',
    'add_module_type',
    'find_module',
]

import logging
from collections import namedtuple

from iga.core import WriteOnceDict


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


_MODULE_TYPES = WriteOnceDict()
_MODULES = WriteOnceDict()


def find_module_type(name):
    return _MODULE_TYPES[name]


def add_module_type(
        *,
        name,
        input_types,
        output_types,
        generate_output_names,
        generate_buildstmts):
    LOG.info('add module type %r', name)
    _MODULE_TYPES[name] = ModuleType(
        name=name,
        input_types=input_types,
        output_types=output_types,
        generate_output_names=generate_output_names,
        generate_buildstmts=generate_buildstmts,
    )


ModuleType = namedtuple('ModuleType', '''
        name
        input_types
        output_types
        generate_output_names
        generate_buildstmts
''')


def find_module(label):
    return _MODULES[label]


def has_module(label):
    return label in _MODULES


def add_module(
        *,
        name,
        type,
        inputs,
        inputs_patterns,
        outputs):
    LOG.info('add module %r', name)
    _MODULES[name] = Module(
        name=name,
        type=type,
        inputs=inputs,
        inputs_patterns=inputs_patterns,
        outputs=outputs,
    )


Module = namedtuple('Module', '''
        name
        type
        inputs
        inputs_patterns
        outputs
''')
