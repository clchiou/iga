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


def parse_argv(argv):
    parser = argparse.ArgumentParser(prog='iga', description='''
    iga meta-build system
    ''')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='verbose output')
    parser.add_argument(
        'label',
        help='build target')
    return parser.parse_args(argv[1:])


def init(args):
    if args.verbose == 0:
        level = logging.WARNING
        format = '%(levelname)s %(message)s'
    elif args.verbose == 1:
        level = logging.INFO
        format = '%(levelname)s %(message)s'
    else:
        level = logging.DEBUG
        format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    logging.basicConfig(level=level, format=format)

    from iga.rules import cc
    cc.init()


def main(argv=None):
    args = parse_argv(argv or sys.argv)

    init(args)
    load_workspace()
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
