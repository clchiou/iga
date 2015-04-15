__all__ = [
    'Rule',
    'RuleData',
    'RuleFunc',
    'RuleType',
]

import logging
from collections import namedtuple

import iga.env
import iga.preconditions
from iga.fargparse import FuncArgsParser
from iga.registry import RegistryMixin


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class RuleType(RegistryMixin):

    @staticmethod
    def make(**kwargs):
        kwargs.setdefault('make_outputs', _make_no_outputs)
        return RuleType(**kwargs)

    def __init__(self,
                 name,
                 input_types,
                 output_types,
                 make_outputs,
                 generate_buildstmts):
        self.name = name
        self.input_types = input_types
        self.output_types = output_types
        self.make_outputs = make_outputs
        self.generate_buildstmts = generate_buildstmts


def _make_no_outputs(_):
    return {}


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
        self.name = name
        self.rule_func = rule_func
        self.parser = parser

    def __call__(self, *args, **kwargs):
        args, kwargs, ignored = self.parser.parse((args, kwargs))
        if ignored:
            LOG.debug('%s ignores %r', self.name, ignored)
        rule_data = self.rule_func(*args, **kwargs)
        iga.preconditions.check_type(rule_data, RuleData)
        iga.env.current()['rule_data'].append(rule_data)


class Rule(RegistryMixin):

    @staticmethod
    def make(rule_data):
        rule_type = RuleType.get_object(rule_data.rule_type)
        rd_inputs = rule_data.inputs or {}
        inputs = {
            input_type: rd_inputs.get(input_type) or []
            for input_type in rule_type.input_types
        }
        rd_outputs = rule_data.outputs or {}
        outputs = {
            output_type: rd_outputs.get(output_type) or []
            for output_type in rule_type.output_types
        }
        return Rule(
            name=rule_data.name,
            rule_type=rule_type,
            inputs=inputs,
            outputs=outputs,
        )

    def __init__(self, name, rule_type, inputs, outputs):
        self.name = name
        self.rule_type = rule_type
        self.inputs = inputs
        self.outputs = outputs

    def write_to(self, ninja_file):
        for buildstmt in self.rule_type.generate_buildstmts(self):
            buildstmt.write_to(ninja_file)


class RuleData(namedtuple('RuleData', '''
        name
        rule_type
        inputs
        input_patterns
        outputs
        ''')):

    @staticmethod
    def make(**kwargs):
        kwargs.setdefault('inputs', ())
        kwargs.setdefault('input_patterns', ())
        kwargs.setdefault('outputs', ())
        return RuleData(**kwargs)
