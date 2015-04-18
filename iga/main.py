__all__ = [
    'main',
]

import argparse
import itertools
import logging
import sys
from collections import OrderedDict

import iga.context
import iga.ninja
import iga.package
from iga.context import load_workspace
from iga.label import Label
from iga.ninja import NinjaRule


logging.basicConfig(level=logging.DEBUG)


def init():
    from iga.lang import cc
    cc.init()


def main(argv=None):
    argv = argv or sys.argv
    init()
    load_workspace()
    parser = argparse.ArgumentParser(prog='iga')
    parser.add_argument('label')
    args = parser.parse_args(argv[1:])
    label = Label.parse_cmdline(args.label)

    rules = OrderedDict()
    ninja_rules = OrderedDict()
    queue = [iga.package.get_rule(label)]
    while queue:
        rule = queue.pop(0)
        if rule.name in rules:
            continue
        rules[rule.name] = rule
        for ninja_rule in rule.rule_type.ninja_rules:
            ninja_rules[ninja_rule] = NinjaRule.get_object(ninja_rule)
        queue.extend(generate_input_rules(rule))

    iga.context.current().update(
        outputs=iga.package.get_outputs(),
        _parsed=True,
    )

    with open('build.ninja', 'w') as ninja_file:
        iga.ninja.write_header_to(ninja_file)
        for ninja_rule in ninja_rules.values():
            ninja_rule.write_to(ninja_file)
        for rule in rules.values():
            rule.write_to(ninja_file)

    return 0


def generate_input_rules(rule):
    for label in itertools.chain.from_iterable(rule.inputs.values()):
        rule = iga.package.get_rule(label, raises=False)
        if rule is not None:
            yield rule
