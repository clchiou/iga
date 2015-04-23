__all__ = [
    'get_outputs',
    'get_rule',
]

import itertools
import logging

import iga.context
import iga.precond
from iga.build_rules import build_rules
from iga.core import WriteOnceDict
from iga.error import IgaError
from iga.path import Glob
from iga.rule import Rule
from iga.rule import RuleFunc


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


# Packages that have been loaded (no BUILD file should be executed twice).
_LOADED_PACKAGES = set()


# Map a rule's outputs to that rule.
_OUTPUT_TO_RULE = WriteOnceDict()


def get_outputs():
    return frozenset(_OUTPUT_TO_RULE)


def get_rule(label, *, raises=False):
    """Return Rule object or raise IgaError (if required, else return
       None) if label does not refer to a rule or an output file.
    """
    if label.package not in _LOADED_PACKAGES:
        _load_rules(label.package)
        _LOADED_PACKAGES.add(label.package)
    rule_label = _OUTPUT_TO_RULE.get(label, label)
    try:
        return Rule.get_object(rule_label)
    except KeyError:
        if raises:
            raise IgaError('%s does not refer to a rule or an output file' %
                           (label,))
    return None


def _load_rules(package):
    """Load rules from a BUILD file."""
    buildfile_path = iga.context.current()['source'] / package / 'BUILD'
    LOG.info('load %s', buildfile_path)
    with buildfile_path.open() as buildfile:
        code = buildfile.read()
    code = compile(code, str(buildfile_path), 'exec')
    rule_data = []
    with iga.context.create() as cxt:
        cxt['package'] = package
        cxt['rule_data'] = rule_data
        exec(code, _make_buildfile_globals())
    for rule in build_rules(package, rule_data):
        Rule.register(rule)
        for output in itertools.chain.from_iterable(rule.outputs.values()):
            _OUTPUT_TO_RULE[output] = rule.name


def _make_buildfile_globals():
    varz = WriteOnceDict()
    varz.update(
        glob=glob,
        package=_do_nothing('package'),
    )
    varz.update(RuleFunc.get_all_objects())
    return dict(varz)


def glob(string):
    iga.precond.check_type(string, str)
    return Glob(string)


def _do_nothing(func_name):
    def func(**kwargs):
        if kwargs:
            LOG.debug('%s() ignores %r', func_name, sorted(kwargs))
    return func
