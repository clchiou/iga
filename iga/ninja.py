__all__ = [
    'add_rule',
    'make_buildstmt',
]

import logging
from collections import namedtuple

from iga.core import WriteOnceDict
from iga.error import IgaError


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


RULE_VARS = (
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


RULE_VARS_V1_3 = (
    'deps',
)


RULE_VARS_V1_5 = (
    'msvc_deps_prefix',
)


RULE_VARS_ALL = RULE_VARS + RULE_VARS_V1_3 + RULE_VARS_V1_5


RESERVED_RULE_NAMES = (
    'phony',
)


_RULES = WriteOnceDict()


def add_rule(*, name, command, **kwargs):
    LOG.info('add rule %r', name)
    variables = kwargs.copy()
    if name in RESERVED_RULE_NAMES:
        raise IgaError('cannot use %r as rule name' % name)
    for key in variables:
        if key not in RULE_VARS_ALL:
            raise IgaError('cannot use %r' % key)
    _RULES[name] = Rule(name=name, command=command, variables=variables)


Rule = namedtuple('Rule', 'name command variables')


def make_buildstmt(
        *,
        rule,
        outputs,
        explicit_deps=None,
        implicit_deps=None,
        orderonly_deps=None,
        variables=None):
    return Buildstmt(
        rule=rule,
        outputs=outputs,
        explicit_deps=explicit_deps,
        implicit_deps=implicit_deps,
        orderonly_deps=orderonly_deps,
        variables=variables)


Buildstmt = namedtuple('Buildstmt', '''
        rule outputs explicit_deps implicit_deps orderonly_deps variables''')
