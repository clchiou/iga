__all__ = [
    'NinjaRule',
]

import iga.preconditions
from iga.registry import RegistryMixin

RULE_VARS_1_0 = (
    'command',
    'depfile',
    'description',
    'generator',
    'in',
    'in_newline',
    'out',
    'restat',
    'rspfile',
    'rspfile_content',
)


RULE_VARS_1_3 = (
    'deps',
)


RULE_VARS_1_5 = (
    'msvc_deps_prefix',
)


RULE_VARS = RULE_VARS_1_0 + RULE_VARS_1_3 + RULE_VARS_1_5


RESERVED_RULE_NAMES = (
    'phony',
)


class NinjaRule(RegistryMixin):

    @staticmethod
    def make(name, command, **kwargs):
        iga.preconditions.check(
            name not in RESERVED_RULE_NAMES,
            'cannot use %r as rule name', name,
        )
        variables = dict(kwargs)
        for key in variables:
            iga.preconditions.check(
                key in RULE_VARS,
                'cannot use %r', key,
            )
        return NinjaRule(name=name, command=command, variables=variables)

    def __init__(self, name, command, variables):
        self.name = name
        self.command = command
        self.variables = variables
