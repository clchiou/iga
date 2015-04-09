__all__ = [
    'Rule',
    'RuleData',
    'RuleFunc',
    'RuleType',
]

import logging
from collections import namedtuple


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class RuleType(namedtuple('RuleType', '''
        name
        input_types
        output_types
        generate_buildstmts
        ''')):

    kind = __name__ + '.RuleType'

    @staticmethod
    def make(**kwargs):
        return RuleType(**kwargs)


class RuleFunc(namedtuple('RuleFunc', 'name rule_func')):

    kind = __name__ + '.RuleFunc'

    @staticmethod
    def make(rule_func):
        # TODO: arg type matcher
        return RuleFunc(
            name=rule_func.__name__,
            rule_func=rule_func,
        )

    def __call__(self, **kwargs):
        LOG.debug('ignore %r', key)


class RuleData(namedtuple('RuleData', 'name type inputs outputs')):

    kind = __name__ + '.RuleData'

    @staticmethod
    def make(**kwargs):
        return RuleData(**kwargs)


class Rule(namedtuple('Rule', 'name')):

    kind = __name__ + '.Rule'

    def write_to(self, ninja_file):
        pass
