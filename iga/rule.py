__all__ = [
    'Rule',
    'RuleData',
    'RuleFunc',
    'RuleType',
]

import logging
from collections import namedtuple

import iga.context
import iga.filetype
import iga.precond
from iga.core import KeyedSets
from iga.fargparse import FuncArgsParser
from iga.registry import RegistryMixin


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class RuleType(RegistryMixin):

    ANY_FILE_TYPE = object()

    @staticmethod
    def make(**kwargs):
        kwargs.setdefault('make_outputs', _make_no_outputs)
        return RuleType(**kwargs)

    def __init__(self,
                 name,
                 input_types,
                 output_types,
                 make_outputs,
                 ninja_rules,
                 generate_buildstmts):
        self.name = name
        self.input_types = input_types
        self.output_types = output_types
        self._make_outputs = make_outputs
        self.ninja_rules = ninja_rules
        self.generate_buildstmts = generate_buildstmts

    def make_outputs(self, inputs):
        if self.output_types is RuleType.ANY_FILE_TYPE:
            outputs = KeyedSets(iga.filetype.get_all())
        else:
            outputs = KeyedSets(self.output_types)
        outputs.update(self._make_outputs(inputs))
        return outputs


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
        iga.precond.check_type(rule_data, RuleData)
        iga.context.current()['rule_data'].append(rule_data)


class Rule(RegistryMixin):

    @staticmethod
    def make(rule_data):
        rule_type = RuleType.get_object(rule_data.rule_type)

        if rule_type.input_types is RuleType.ANY_FILE_TYPE:
            inputs = KeyedSets(iga.filetype.get_all())
        else:
            inputs = KeyedSets(rule_type.input_types)
        inputs.update(rule_data.inputs)

        if rule_type.output_types is RuleType.ANY_FILE_TYPE:
            outputs = KeyedSets(iga.filetype.get_all())
        else:
            outputs = KeyedSets(rule_type.output_types)
        outputs.update(rule_data.outputs)

        return Rule(
            name=rule_data.name,
            rule_type=rule_type,
            inputs=inputs,
            outputs=outputs,
            variables=rule_data.variables,
        )

    def __init__(self, name, rule_type, inputs, outputs, variables):
        self.name = name
        self.rule_type = rule_type
        self.inputs = inputs
        self.outputs = outputs
        self.variables = variables

    def write_to(self, ninja_file):
        for buildstmt in self.rule_type.generate_buildstmts(self):
            buildstmt.write_to(ninja_file)


class RuleData(namedtuple('RuleData', '''
        name
        rule_type
        inputs
        input_patterns
        outputs
        variables
        ''')):

    @staticmethod
    def make(**kwargs):
        kwargs.setdefault('inputs', {})
        kwargs.setdefault('input_patterns', [])
        kwargs.setdefault('outputs', {})
        kwargs.setdefault('variables', {})
        return RuleData(**kwargs)
