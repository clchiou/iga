__all__ = [
    'Rule',
    'RuleData',
    'RuleFunc',
    'RuleType',
]

import logging
from collections import namedtuple

from iga.matcher import KwargsMatcher
from iga.registry import RegistryMixin


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class RuleType(namedtuple('RuleType', '''
        name
        input_types
        output_types
        generate_buildstmts
        '''), RegistryMixin):

    @staticmethod
    def make(**kwargs):
        return RuleType(**kwargs)


class RuleFunc(namedtuple('RuleFunc', 'name rule_func kwargs_matcher'),
               RegistryMixin):

    @staticmethod
    def make(rule_func):
        kwargs_matcher = KwargsMatcher.parse(rule_func)
        return RuleFunc(
            name=rule_func.__name__,
            rule_func=rule_func,
            kwargs_matcher=kwargs_matcher,
        )

    def __call__(self, **kwargs):
        matched_kwargs, ignored = self.kwargs_matcher.match(kwargs)
        LOG.debug('%s ignores %r', self.name, ignored)
        return self.rule_func(**matched_kwargs)


class RuleData(namedtuple('RuleData', 'name type inputs outputs'),
               RegistryMixin):

    @staticmethod
    def make(**kwargs):
        return RuleData(**kwargs)


class Rule(namedtuple('Rule', 'name'),
           RegistryMixin):

    def write_to(self, ninja_file):
        pass
