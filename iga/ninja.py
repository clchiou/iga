__all__ = [
    'add_ninja_rule',
    'get_ninja_rule',
]

import logging
from collections import namedtuple

import iga.env
from iga.core import WriteOnceDict
from iga.error import IgaError


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


NinjaRule = namedtuple('NinjaRule', 'name command variables')


# Registry of rules.


iga.env.root()[__name__] = WriteOnceDict()


def _ninja_rules():
    return iga.env.root()[__name__]


def add_ninja_rule(*, name, command, **kwargs):
    LOG.info('add ninja rule %r', name)
    variables = dict(kwargs)
    if name in RESERVED_RULE_NAMES:
        raise IgaError('cannot use %r as rule name' % name)
    for key in variables:
        if key not in RULE_VARS_ALL:
            raise IgaError('cannot use %r' % key)
    _ninja_rules()[name] = NinjaRule(
        name=name, command=command, variables=variables,
    )


def get_ninja_rule(name):
    return _ninja_rules()[name]
