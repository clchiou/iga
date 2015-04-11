__all__ = [
    'Rule',
    'RuleData',
    'RuleFunc',
    'RuleType',
]

import logging

from iga.matcher import KwargsMatcher
from iga.registry import RegistryMixin


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class RuleType(RegistryMixin):

    @staticmethod
    def make(**kwargs):
        return RuleType(**kwargs)

    def __init__(self,
                 name,
                 input_types,
                 output_types,
                 generate_buildstmts):
        self.name = name
        self.input_types = input_types
        self.output_types = output_types
        self.generate_buildstmts = self.generate_buildstmts


class RuleFunc(RegistryMixin):

    @staticmethod
    def make(rule_func):
        kwargs_matcher = KwargsMatcher.parse(rule_func)
        return RuleFunc(
            name=rule_func.__name__,
            rule_func=rule_func,
            kwargs_matcher=kwargs_matcher,
        )

    def __init__(self,
                 name,
                 rule_func,
                 kwargs_matcher):
        self.name = self.name
        self.rule_func = rule_func
        self.kwargs_matcher = kwargs_matcher

    def __call__(self, **kwargs):
        matched_kwargs, ignored = self.kwargs_matcher.match(kwargs)
        LOG.debug('%s ignores %r', self.name, ignored)
        return self.rule_func(**matched_kwargs)


class RuleData(RegistryMixin):

    @staticmethod
    def make(**kwargs):
        return RuleData(**kwargs)

    def __init__(self,
                 name,
                 rule_type,
                 inputs,
                 outputs):
        self.name = name
        self.rule_type = rule_type
        self.inputs = inputs
        self.outputs = outputs


class Rule(RegistryMixin):

    def __init__(self, name):
        self.name = self.name

    def write_to(self, ninja_file):
        pass
