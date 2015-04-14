__all__ = [
    'get_rule',
    'get_rule_or_none',
]

import itertools
import logging

import iga.env
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
    buildfile_path = iga.env.root()['source'] / package / 'BUILD'
    LOG.info('load %s', buildfile_path)
    with buildfile_path.open() as buildfile:
        code = buildfile.read()
    code = compile(code, str(buildfile_path), 'exec')
    rule_data = []
    with iga.env.enter_child_env() as child_env:
        child_env['package'] = package
        child_env['rule_data'] = rule_data
        exec(code, _make_context())
    return build_rules(package, rule_data)


def _make_context():
    context = WriteOnceDict()
    context.update(_BUILTINS)
    context.update(RuleFunc.get_all_objects())
    return dict(context)


def _make_context_func(func_name):
    """Make functions executed inside BUILD evaluation context."""
    def func(**kwargs):
        if kwargs:
            LOG.debug('%s() ignores %r', func_name, sorted(kwargs))
    return func


_BUILTINS = {
    'package': _make_context_func('package'),
}
