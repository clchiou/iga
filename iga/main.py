__all__ = [
    'main',
]

import argparse
import itertools
import logging
import sys

import iga.env
import iga.label
import iga.rule
from iga.core import ImmutableOrderedSet


# Good for debugging
logging.basicConfig(level=logging.DEBUG)


def main(argv=None):
    argv = argv or sys.argv
    parser = argparse.ArgumentParser(prog='iga')
    parser.add_argument('label')
    args = parser.parse_args(argv[1:])
    label = iga.label.parse_label(args.label)
    queue = [iga.rule.get_rule(label)]
    with open('build.ninja', 'w') as ninja_file:
        while queue:
            rule = queue.pop(0)
            rule.write_to(ninja_file)
            queue.extend(ImmutableOrderedSet(generate_input_rules(rule)))
    return 0


def generate_input_rules(rule):
    for label in itertools.chain.from_iterable(rule.inputs.values()):
        yield iga.rule.get_rule(label)
