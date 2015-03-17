import argparse
import itertools
import logging

import iga.label
import iga.module
import iga.ninja
import iga.package
from iga.core import ImmutableOrderedSet


# Good for debugging
logging.basicConfig(level=logging.DEBUG)


def main(argv):
    parser = argparse.ArgumentParser(prog='iga')
    parser.add_argument('label')
    args = parser.parse_args(argv[1:])
    label = iga.label.parse_label(args.label)
    iga.package.load_package(label.package)
    modules = [iga.module.find_module(label)]
    i = 0
    while i < len(modules):
        for _, inputs in modules[i].inputs.items():
            for mod_label in inputs:
                if not isinstance(mod_label, iga.label.ModuleLabel):
                    continue
                if not iga.module.has_module(mod_label):
                    iga.package.load_package(mod_label.package)
                modules.append(iga.module.find_module(mod_label))
        i = i + 1
    rule_names = ImmutableOrderedSet(itertools.chain.from_iterable(
        iga.module.find_module_type(module.type).rules for module in modules
    ))
    for rule_name in rule_names:
        print(iga.ninja.find_rule(rule_name))
    for module in modules:
        module_type = iga.module.find_module_type(module.type)
        for buildstmt in module_type.generate_buildstmts(module):
            print(buildstmt)
    return 0
