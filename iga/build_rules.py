__all__ = [
    'build_rules',
]

import itertools
from collections import defaultdict

import iga.env
from iga.core import ImmutableOrderedSet
from iga.core import list_difference
from iga.rule import Rule


def build_rules(package, rule_datas, *, _env=None):
    """Build Rule objects from a list of RuleData iteratively."""
    env = _env or iga.env.current()
    srcdir = env['source'] / package
    outdir = env['build'] / package
    rules = {rule_data.name: Rule.make(rule_data) for rule_data in rule_datas}
    # Glob inputs.
    for rule_data in rule_datas:
        rule = rules[rule_data.name]
        pathsets_by_type = glob_by_type(
            rule.rule_type.input_types, rule_data.input_patterns, srcdir
        )
        for input_type, pathset in pathsets_by_type.items():
            rule.inputs[input_type].extend(pathset)
    # Generate outputs from current inputs.
    added_pathsets_by_type = defaultdict(set)
    for rule in rules.values():
        update_pathsets(
            added_pathsets_by_type, _gen_outputs(rule.inputs, rule)
        )
    # Iteratively update inputs.
    while is_not_empty(added_pathsets_by_type):
        paths_by_type = {
            path_type: sorted(pathset)
            for path_type, pathset in added_pathsets_by_type.items()
        }
        added_pathsets_by_type = defaultdict(set)
        for rule_data in rule_datas:
            rule = rules[rule_data.name]
            update_pathsets(
                added_pathsets_by_type,
                _match_inputs(rule_data, paths_by_type, outdir, rule),
            )
    return [rules[rule_data.name] for rule_data in rule_datas]


def is_not_empty(pathsets_by_type):
    return any(pathset for pathset in pathsets_by_type.values())


def glob_by_types(types, patterns_by_type, dirpath):
    pathsets_by_type = {}
    for typ in types:
        pathset = ImmutableOrderedSet(itertools.chain.from_iterable(
            pattern.glob(dirpath) for pattern in patterns_by_type.get(typ, ())
        ))
        pathsets_by_type[typ] = pathset
    return pathsets_by_type


def _match_inputs(rule_data, paths_by_type, outdir, rule):
    added_pathset_by_type = defaultdict(set)
    for input_type in rule.inputs:
        inputs = set()
        for pattern in rule_data.input_patterns.get(input_type, ()):
            inputs.update(
                filter(pattern.match, paths_by_type.get(input_type, ()))
            )
        inputs = sorted(outdir / path for path in inputs)
        adding = list_difference(inputs, rule.inputs[input_type])
        rule.inputs[input_type].extend(adding)
        added_pathset_by_type[input_type].update(adding)
    return added_pathset_by_type


def _gen_outputs(inputs_by_type, rule):
    added_pathset_by_type = defaultdict(set)
    outputs_by_type = rule.rule_type.make_outputs(inputs_by_type)
    for output_type, outputs in outputs_by_type.items():
        adding = list_difference(outputs, rule.outputs[output_type])
        rule.outputs[output_type].extend(adding)
        added_pathset_by_type[output_type].update(adding)
    return added_pathset_by_type


def update_pathsets(pathsets_by_type, more_pathsets_by_type):
    for path_type, pathset in more_pathsets_by_type.items():
        pathsets_by_type[path_type].update(pathset)
