__all__ = [
    'main',
]

import argparse
import itertools
import logging
import sys

import iga.package
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
    label = Label.parse_cmdline(args.label)
    queue = [iga.package.get_rule(label)]
    with open('build.ninja', 'w') as ninja_file:
        while queue:
            rule = queue.pop(0)
            rule.write_to(ninja_file)
            queue.extend(ImmutableOrderedSet(generate_input_rules(rule)))
    return 0


def generate_input_rules(rule):
    for label in itertools.chain.from_iterable(rule.inputs.values()):
        yield iga.package.get_rule(label)
