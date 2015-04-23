"""Build rules for C/C++."""

__all__ = [
    'init',
]

import itertools

import iga.filetype
from iga.core import ImmutableOrderedSet
from iga.core import group
from iga.core import traverse
from iga.fargparse import oneof
from iga.label import Label
from iga.ninja import NinjaBuildstmt
from iga.ninja import NinjaRule
from iga.path import Glob
from iga.rule import Rule
from iga.rule import RuleData
from iga.rule import RuleFunc
from iga.rule import RuleType


CC_SOURCE = 'cc_source'
CC_HEADER = 'cc_header'
CC_OBJECT = 'cc_object'
CC_LIBRARY = 'cc_library'
CC_BINARY = 'cc_binary'


CC_SUFFIXES = {
    CC_LIBRARY: {'.a'},
    CC_SOURCE: {'.c', '.cc', '.cpp', '.cxx', '.C'},
    CC_HEADER: {'.h', '.hh', '.hpp', '.hxx', '.inc'},
}


def init():
    """Init C/C++ build rules."""
    NinjaRule.register(NinjaRule.make(
        name=CC_OBJECT,
        command='$cxx -MMD -MT $out -MF $out.d $cflags -c $in -o $out',
        description='CXX $out',
        depfile='$out.d',
        deps='gcc',
    ))
    NinjaRule.register(NinjaRule.make(
        name=CC_LIBRARY,
        command='rm -f $out && $ar crs $out $in',
        description='AR $out',
    ))
    NinjaRule.register(NinjaRule.make(
        name=CC_BINARY,
        command='$cxx $ldflags -o $out $in $libs',
        description='LINK $out',
    ))

    for input_type, suffixes in CC_SUFFIXES.items():
        for suffix in suffixes:
            iga.filetype.add_suffix(input_type, suffix)

    RuleType.register(RuleType.make(
        name=CC_LIBRARY,
        input_types=[CC_LIBRARY, CC_SOURCE, CC_HEADER],
        output_types=[CC_LIBRARY, CC_OBJECT],
        make_outputs=make_outputs,
        ninja_rules=[CC_OBJECT, CC_LIBRARY],
        generate_buildstmts=generate_library,
    ))
    RuleType.register(RuleType.make(
        name=CC_BINARY,
        input_types=[CC_LIBRARY, CC_SOURCE, CC_HEADER],
        output_types=[CC_BINARY, CC_OBJECT],
        make_outputs=make_outputs,
        ninja_rules=[CC_OBJECT, CC_BINARY],
        generate_buildstmts=generate_binary,
    ))

    RuleFunc.register(RuleFunc.make(cc_library))
    RuleFunc.register(RuleFunc.make(cc_binary))


def make_outputs(inputs):
    return {
        CC_OBJECT: [
            src.with_suffix('.o') for src in inputs[CC_SOURCE]
        ],
    }


def cc_library(
        name: Label,
        srcs: [oneof(Label, Glob)]=(),
        deps: [Label]=()):
    srcs = group(srcs, key=type, as_dict=False)
    inputs = group(srcs[Label], key=iga.filetype.get, as_dict=False)
    inputs[CC_LIBRARY] += deps
    return RuleData.make(
        rule_type=CC_LIBRARY,
        name=name,
        inputs=inputs,
        input_patterns=srcs[Glob],
        outputs={CC_LIBRARY: [name.with_name(_lib(name.name))]},
    )


def cc_binary(
        name: Label,
        srcs: [oneof(Label, Glob)]=(),
        deps: [Label]=()):
    srcs = group(srcs, key=type, as_dict=False)
    inputs = group(srcs[Label], key=iga.filetype.get, as_dict=False)
    inputs[CC_LIBRARY] += deps
    return RuleData.make(
        rule_type=CC_BINARY,
        name=name,
        inputs=inputs,
        input_patterns=srcs[Glob],
        outputs={CC_BINARY: [name]},
    )


def generate_objects(rule):
    headers = rule.inputs[CC_HEADER]
    for src in rule.inputs[CC_SOURCE]:
        yield NinjaBuildstmt.make(
            ninja_rule=CC_OBJECT,
            outputs=[src.with_suffix('.o')],
            explicit_deps=[src],
            implicit_deps=headers,
        )


def generate_library(rule):
    yield from generate_objects(rule)
    yield NinjaBuildstmt.make(
        ninja_rule=CC_LIBRARY,
        outputs=rule.outputs[CC_LIBRARY],
        explicit_deps=rule.outputs[CC_OBJECT],
    )


def generate_binary(rule):
    yield from generate_objects(rule)
    # Retrieve the transitive closure of dependent CC_LIBRARY rules.
    deps = list(map(
        Rule.get_object,
        ImmutableOrderedSet(itertools.chain.from_iterable(
            traverse(label, _get_labels) for label in rule.inputs[CC_LIBRARY]
        ))
    ))
    outputs = [label for dep in deps for label in dep.outputs[CC_LIBRARY]]
    ldflags = ' '.join('-L%s' % label.path.parent for label in outputs)
    libs = ' '.join('-l%s' % _unlib(label.name) for label in outputs)
    yield NinjaBuildstmt.make(
        ninja_rule=CC_BINARY,
        outputs=rule.outputs[CC_BINARY],
        explicit_deps=rule.outputs[CC_OBJECT],
        implicit_deps=outputs,
        variables={
            'ldflags': '$ldflags ' + ldflags,
            'libs': libs,
        },
    )


def _get_labels(label):
    rule = Rule.get_object(label)
    return [Rule.get_object(label).name for label in rule.inputs[CC_LIBRARY]]


def _lib(name):
    return 'lib%s.a' % name


def _unlib(name):
    """Inverse of _lib()."""
    assert name.startswith('lib') and name.endswith('.a')
    return name[3:-2]
