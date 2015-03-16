__all__ = [
    'add_module',
    'add_module_type',
    'find_module',
]

from collections import namedtuple

from iga.core import WriteOnceDict


_MODULE_TYPES = WriteOnceDict()
_MODULES = WriteOnceDict()


def add_module_type(*, name, input_types, output_types, generate_buildstmts):
    _MODULE_TYPES[name] = ModuleType(
        name=name,
        input_types=input_types,
        output_types=output_types,
        generate_buildstmts=generate_buildstmts,
    )


ModuleType = namedtuple('ModuleType', '''
        name input_types output_types generate_buildstmts''')


def find_module(label):
    """Find module by label."""
    return _MODULES[label]


def add_module(*, name, type, inputs, outputs):
    _MODULES[name] = Module(
        name=name,
        type=type,
        inputs=inputs,
        outputs=outputs,
    )


Module = namedtuple('Module', 'name type inputs outputs')
