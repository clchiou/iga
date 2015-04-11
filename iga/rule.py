__all__ = [
    'Rule',
    'RuleData',
    'RuleFunc',
    'RuleType',
]

import logging

from iga.fargparse import FuncArgsParser
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
        parser = FuncArgsParser.make(rule_func)
        return RuleFunc(
            name=rule_func.__name__,
            rule_func=rule_func,
            parser=parser,
        )

    def __init__(self,
                 name,
                 rule_func,
                 parser):
        self.name = self.name
        self.rule_func = rule_func
        self.parser = parser

    def __call__(self, *args, **kwargs):
        args, kwargs, ignored = self.parser.parse((args, kwargs))
        LOG.debug('%s ignores %r', self.name, ignored)
        return self.rule_func(*args, **kwargs)


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
