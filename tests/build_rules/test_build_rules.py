import unittest
from pathlib import Path
from pathlib import PurePosixPath

import iga.registry
from iga.build_rules import build_rules
from iga.label import Label
from iga.path import Glob
from iga.rule import Rule
from iga.rule import RuleData
from iga.rule import RuleType


class TestBuildRules(unittest.TestCase):

    def setUp(self):
        iga.registry.reset()

    def tearDown(self):
        iga.registry.reset()

    def test_build_rules(self):
        def make_outputs(ksets):
            return {
                'ot-1': ksets['ot-1'] | ksets['it-1'],
                'ot-2': ksets['ot-2'] | ksets['it-2'],
            }

        def get_file_type(label):
            return label.suffix[1:]

        RuleType.register(RuleType.make(
            name='rule-type',
            input_types=['it-1', 'it-2', 'ot-1', 'ot-2'],
            output_types=['ot-1', 'ot-2'],
            make_outputs=make_outputs,
            ninja_rules=[],
            generate_buildstmts=None,
        ))

        package = 'a/b/c'
        cxt = {'source': Path(__file__).parent / 'test-data/src'}
        rule_datas = [
            RuleData.make(
                name=Label.make(package, 'rule-1'),
                rule_type='rule-type',
                inputs={
                    'it-1': [
                        Label.make(package, 'ival-11'),
                        Label.make(package, 'ival-12'),
                    ],
                    'it-2': [
                        Label.make(package, 'ival-21'),
                    ],
                },
                input_patterns=[Glob('ival-*')],
                outputs={
                    'ot-1': [
                        Label.make(package, 'output-1'),
                    ],
                    'ot-2': [
                        Label.make(package, 'output-2'),
                    ],
                },
            ),
            RuleData.make(
                name=Label.make(package, 'rule-2'),
                rule_type='rule-type',
                outputs={
                    'ot-1': [
                        Label.make(package, 'ival-rule-2-11.ot-1'),
                        Label.make(package, 'ival-rule-2-12.ot-1'),
                    ],
                    'ot-2': [
                        Label.make(package, 'ival-rule-2-21.ot-2'),
                        Label.make(package, 'ival-rule-2-22.ot-2'),
                        Label.make(package, 'ival-rule-2-23.ot-2'),
                    ],
                },
            ),
        ]

        rules = build_rules(package, rule_datas,
                            _cxt=cxt, _get_file_type=get_file_type)
        self.assertEqual(2, len(rules))
        self.assertRuleEqual(
            Rule(
                name=Label.make(package, 'rule-1'),
                rule_type=RuleType.get_object('rule-type'),
                inputs={
                    'it-1': {
                        Label.make(package, 'ival-11'),
                        Label.make(package, 'ival-12'),
                    },
                    'it-2': {
                        Label.make(package, 'ival-21'),
                    },
                    'ot-1': {
                        Label.make(package, 'ival-rule-2-11.ot-1'),
                        Label.make(package, 'ival-rule-2-12.ot-1'),
                    },
                    'ot-2': {
                        Label.make(package, 'ival-rule-2-21.ot-2'),
                        Label.make(package, 'ival-rule-2-22.ot-2'),
                        Label.make(package, 'ival-rule-2-23.ot-2'),
                    },
                },
                outputs={
                    'ot-1': {
                        Label.make(package, 'output-1'),
                        Label.make(package, 'ival-11'),
                        Label.make(package, 'ival-12'),
                        Label.make(package, 'ival-rule-2-11.ot-1'),
                        Label.make(package, 'ival-rule-2-12.ot-1'),
                    },
                    'ot-2': {
                        Label.make(package, 'output-2'),
                        Label.make(package, 'ival-21'),
                        Label.make(package, 'ival-rule-2-21.ot-2'),
                        Label.make(package, 'ival-rule-2-22.ot-2'),
                        Label.make(package, 'ival-rule-2-23.ot-2'),
                    },
                },
                variables={},
            ),
            rules[0],
        )

    def assertRuleEqual(self, expected, actual):
        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.rule_type, actual.rule_type)
        self.assertEqual(expected.inputs, actual.inputs.as_dict_of_sets())
        self.assertEqual(expected.outputs, actual.outputs.as_dict_of_sets())


if __name__ == '__main__':
    unittest.main()
