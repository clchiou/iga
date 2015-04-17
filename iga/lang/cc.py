"""Build rules for C/C++."""

__all__ = [
    'init',
]

from iga.core import group
from iga.fargparse import oneof
from iga.label import Label
from iga.ninja import NinjaBuildstmt
from iga.ninja import NinjaRule
from iga.path import Glob
from iga.rule import RuleData
from iga.rule import RuleFunc
from iga.rule import RuleType


CC_SOURCE = 'cc_source'
CC_OBJECT = 'cc_object'
CC_DEPEND = 'cc_depend'
CC_LIBRARY = 'cc_library'
CC_BINARY = 'cc_binary'


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

    RuleType.register(RuleType.make(
        name=CC_LIBRARY,
        input_types=[CC_LIBRARY, CC_SOURCE],
        output_types=[CC_LIBRARY, CC_OBJECT, CC_DEPEND],
        make_outputs=make_outputs,
        ninja_rules=[CC_OBJECT, CC_LIBRARY],
        generate_buildstmts=generate_library,
    ))
    RuleType.register(RuleType.make(
        name=CC_BINARY,
        input_types=[CC_LIBRARY, CC_SOURCE],
        output_types=[CC_BINARY, CC_OBJECT, CC_DEPEND],
        make_outputs=make_outputs,
        ninja_rules=[CC_OBJECT, CC_BINARY],
        generate_buildstmts=generate_binary,
    ))

    RuleFunc.register(RuleFunc.make(cc_binary))
    RuleFunc.register(RuleFunc.make(cc_library))


def make_outputs(inputs):
    return {
        CC_OBJECT: [
            src.with_suffix('.o') for src in inputs[CC_SOURCE]
        ],
        CC_DEPEND: [
            src.with_suffix('.o.d') for src in inputs[CC_SOURCE]
        ],
    }


def cc_library(
        name: Label,
        srcs: [oneof(Label, Glob)]=(),
        deps: [Label]=()):
    srcs = group(srcs, key=type, as_dict=False)
    return RuleData.make(
        rule_type=CC_LIBRARY,
        name=name,
        inputs={
            CC_LIBRARY: deps,
            CC_SOURCE: srcs[Label],
        },
        input_patterns={
            CC_SOURCE: srcs[Glob],
        },
        outputs={
            CC_LIBRARY: [name.with_name(to_libname(name.name))],
        },
    )


def cc_binary(
        name: Label,
        srcs: [oneof(Label, Glob)]=(),
        deps: [Label]=()):
    srcs = group(srcs, key=type, as_dict=False)
    return RuleData.make(
        rule_type=CC_BINARY,
        name=name,
        inputs={
            CC_LIBRARY: deps,
            CC_SOURCE: srcs[Label],
        },
        input_patterns={
            CC_SOURCE: srcs[Glob],
        },
        outputs={
            CC_BINARY: [name],
        },
    )


def generate_objects(rule):
    for src in rule.inputs[CC_SOURCE]:
        yield NinjaBuildstmt.make(
            ninja_rule=CC_OBJECT,
            outputs=[src.with_suffix('.o')],
            explicit_deps=[src],
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
    libs = [
        lib.with_name(to_libname(lib.name))
        for lib in rule.inputs[CC_LIBRARY]
    ]
    ldflags = ' '.join(
        '-L%s' % lib.path.parent for lib in rule.inputs[CC_LIBRARY]
    )
    llibs = ' '.join(
        '-l%s' % lib.name for lib in rule.inputs[CC_LIBRARY]
    )
    yield NinjaBuildstmt.make(
        ninja_rule=CC_BINARY,
        outputs=rule.outputs[CC_BINARY],
        explicit_deps=rule.outputs[CC_OBJECT],
        implicit_deps=libs,
        variables={
            'ldflags': '$ldflags ' + ldflags,
            'libs': llibs,
        },
    )


def to_libname(name):
    """X -> libX.a"""
    return 'lib%s.a' % name
