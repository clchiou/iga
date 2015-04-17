__all__ = [
    'main',
]

import argparse
import itertools
import logging
import sys

import iga.ninja
import iga.package
from iga.core import ImmutableOrderedSet
from iga.label import Label
from iga.ninja import NinjaRule

# Good for debugging
logging.basicConfig(level=logging.DEBUG)


def init():
    from iga.lang import cc
    cc.init()


def main(argv=None):
    argv = argv or sys.argv
    init()
    parser = argparse.ArgumentParser(prog='iga')
    parser.add_argument('label')
    args = parser.parse_args(argv[1:])
    label = Label.parse_cmdline(args.label)
    queue = [iga.package.get_rule(label)]
    rules = set()
    ninja_rules = set()
    with open('build.ninja', 'w') as ninja_file:
        iga.ninja.write_header_to(ninja_file)
        while queue:
            rule = queue.pop(0)
            if rule.name in rules:
                continue
            for ninja_rule in rule.rule_type.ninja_rules:
                if ninja_rule not in ninja_rules:
                    NinjaRule.get_object(ninja_rule).write_to(ninja_file)
                    ninja_rules.add(ninja_rule)
            rule.write_to(ninja_file)
            queue.extend(ImmutableOrderedSet(generate_input_rules(rule)))
            rules.add(rule.name)
    return 0


def generate_input_rules(rule):
    for label in itertools.chain.from_iterable(rule.inputs.values()):
        rule = iga.package.get_rule_or_none(label)
        if rule is not None:
            yield rule
