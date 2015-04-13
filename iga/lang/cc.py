"""Build rules for C/C++."""

__all__ = [
    'init',
]

from iga.core import group
from iga.fargparse import oneof
from iga.label import Label
from iga.ninja import NinjaRule
from iga.path import Glob
from iga.rule import RuleData
from iga.rule import RuleFunc
from iga.rule import RuleType


CC_SOURCE = 'cc_source'
CC_COMPILE = 'cc_compile'
CC_LIBRARY = 'cc_library'
CC_BINARY = 'cc_binary'


CC_SOURCE_SUFFIXES = ('.c', '.cc', '.cpp', '.cxx', 'C')
CC_HEADER_SUFFIXES = ('.h', '.hh', '.hpp', '.hxx', '.inc')
CC_SUFFIXES = CC_SOURCE_SUFFIXES + CC_HEADER_SUFFIXES


def init():
    """Init C/C++ build rules."""
    NinjaRule.register(NinjaRule.make(
        name=CC_COMPILE,
        command='$cc $cflags -c $in -o $out',
        description='CC $out',
    ))
    NinjaRule.register(NinjaRule.make(
        name=CC_LIBRARY,
        command='rm -f $out && $ar crs $out $in',
        description='AR $out',
    ))
    NinjaRule.register(NinjaRule.make(
        name=CC_BINARY,
        command='$cc $ldflags -o $out $in $libs',
        description='LINK $out',
    ))

    RuleType.register(RuleType.make(
        name=CC_LIBRARY,
        input_types=[CC_LIBRARY, CC_SOURCE],
        output_types=[CC_LIBRARY],
        generate_buildstmts=generate_library,
    ))
    RuleType.register(RuleType.make(
        name=CC_BINARY,
        input_types=[CC_LIBRARY, CC_SOURCE],
        output_types=[CC_BINARY],
        generate_buildstmts=generate_binary,
    ))

    RuleFunc.register(RuleFunc.make(cc_binary))
    RuleFunc.register(RuleFunc.make(cc_library))


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


def generate_binary():
    pass


def generate_library():
    pass


def to_libname(name):
    """X -> libX.a"""
    return 'lib%s.a' % name
