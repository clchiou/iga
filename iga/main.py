__all__ = [
    'main',
]

import argparse
import itertools
import logging
import sys
from pathlib import Path

import iga.env
import iga.package
import iga.workspace
from iga.core import ImmutableOrderedSet
from iga.label import Label

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
    if 'root' not in iga.env.current():
        iga.workspace.workspace(root=Path.cwd())
    label = Label.parse_cmdline(args.label)
    queue = [iga.package.get_rule(label)]
    rule_names = set()
    with open('build.ninja', 'w') as ninja_file:
        while queue:
            rule = queue.pop(0)
            if rule.name in rule_names:
                continue
            rule.write_to(ninja_file)
            queue.extend(ImmutableOrderedSet(generate_input_rules(rule)))
            rule_names.add(rule.name)
    return 0


def generate_input_rules(rule):
    for label in itertools.chain.from_iterable(rule.inputs.values()):
        rule = iga.package.get_rule_or_none(label)
        if rule is not None:
            yield rule
