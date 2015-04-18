"""Iteratively build Rule objects from RuleData objects."""

__all__ = [
    'build_rules',
]

import itertools

import iga.context
from iga.core import KeyedSets
from iga.label import Label
from iga.rule import Rule


def build_rules(package, rule_datas, *, _cxt=None):
    """Build Rule objects from a list of RuleData iteratively."""
    srcdir = (_cxt or iga.context.current())['source']
    rules = [Rule.make(rule_data) for rule_data in rule_datas]
    # Glob source directory.
    for rule, rule_data in zip(rules, rule_datas):
        rule.inputs.update(glob_keyed_sets(
            rule.inputs.keys(),
            rule_data.input_patterns,
            srcdir,
            package,
        ))
    # Make outputs from inputs.
    for rule in rules:
        rule.outputs.update(rule.rule_type.make_outputs(rule.inputs))
    # Iteratively update inputs from other rules' outputs.
    added_outputs = {rule.name: rule.outputs for rule in rules}
    while added_outputs:
        added_inputs = []
        for rule, rule_data in zip(rules, rule_datas):
            adding = KeyedSets(rule.inputs.keys())
            # Gather outputs from other rules.
            for name, outputs in added_outputs.items():
                if name != rule.name:
                    adding.update(outputs)
            # Match against this rule's input_patterns.
            adding = match_keyed_sets(adding, rule_data.input_patterns)
            # Remove labels that are already there.
            adding.difference_update(rule.inputs)
            # If it's still non-empty, then changed is True.
            if adding:
                added_inputs.append((rule, adding))
        # Update inputs and make outputs from newly-added inputs.
        added_outputs = {}
        for rule, adding in added_inputs:
            rule.inputs.update(adding)
            outputs = rule.rule_type.make_outputs(adding)
            if outputs:
                rule.outputs.update(outputs)
                added_outputs[rule.name] = outputs
    return rules


def glob_keyed_sets(keys, patterns, from_dir, package):
    ksets = KeyedSets(keys)
    package_dir = from_dir / package
    for key in ksets:
        paths = itertools.chain.from_iterable(
            pattern.glob(package_dir) for pattern in patterns.get(key, ())
        )
        labels = (_path_to_label(path, from_dir, package) for path in paths)
        ksets[key].update(labels)
    return ksets


def match_keyed_sets(ksets, patterns):
    result = KeyedSets(ksets.keys())
    for key in ksets:
        for pattern in patterns.get(key, ()):
            result[key].update(
                label for label in ksets[key] if pattern.match(label.target)
            )
    return result


def _path_to_label(path, root, package):
    target = path.relative_to(root / package)
    return Label.make(package, target)
