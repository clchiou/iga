__all__ = [
    'get_rule',
    'get_rule_or_none',
]

import itertools
import logging

import iga.context
from iga.build_rules import build_rules
from iga.core import WriteOnceDict
from iga.error import IgaError
from iga.rule import Rule
from iga.rule import RuleFunc


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


_LOADED_PACKAGES = set()
_FILE_LABLE_TO_RULE_NAME = WriteOnceDict()


def get_rule(label):
    """Return Rule object or raise IgaError if label points to non-rule."""
    rule = get_rule_or_none(label)
    if rule is None:
        raise IgaError('%s is not a build rule' % (label,))
    return rule


def get_rule_or_none(label):
    """Return Rule object or raise IgaError if label points to non-rule."""
    if label.package not in _LOADED_PACKAGES:
        for rule in _load_rules(label.package):
            Rule.register(rule)
            for output in itertools.chain.from_iterable(rule.outputs.values()):
                _FILE_LABLE_TO_RULE_NAME[output] = rule.name
        _LOADED_PACKAGES.add(label.package)
    # If label points to a file, find the rule generating that file.
    label = _FILE_LABLE_TO_RULE_NAME.get(label, label)
    try:
        return Rule.get_object(label)
    except KeyError:
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
    return build_rules(package, rule_data)


def _make_buildfile_globals():
    varz = WriteOnceDict()
    varz.update(
        package=_do_nothing('package'),
    )
    varz.update(RuleFunc.get_all_objects())
    return dict(varz)


def _do_nothing(func_name):
    def func(**kwargs):
        if kwargs:
            LOG.debug('%s() ignores %r', func_name, sorted(kwargs))
    return func
