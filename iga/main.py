__all__ = [
    'main',
]

import argparse
import logging
import sys

import iga.label
import iga.module
import iga.ninja
import iga.package


# Good for debugging
logging.basicConfig(level=logging.DEBUG)


def main(argv=None):
    argv = argv or sys.argv
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
    generated_rules = set()
    for module in modules:
        module_type = iga.module.find_module_type(module.type)
        for buildstmt in module_type.generate_buildstmts(module):
            if buildstmt.rule not in generated_rules:
                print(iga.ninja.find_rule(buildstmt.rule))
                generated_rules.add(buildstmt.rule)
            print(buildstmt)
    return 0
