__all__ = [
    'get_rule',
]

import logging

import iga.env
import iga.rule
from iga.core import WriteOnceDict
from iga.rule import Rule
from iga.rule import RuleFunc


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


_PACKAGES = set()


def get_rule(label):
    # TODO: XXX: If label is a file, not a rule, you should not return stuff?
    try:
        return Rule.get_object(label)
    except KeyError:
        pass
    assert label.package not in _PACKAGES
    for rule in _load_rules(label.package):
        Rule.register(rule)
    _PACKAGES.add(label.package)
    return Rule.get_object(label)


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
    return iga.rule.build_rules(package, rule_data)


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
