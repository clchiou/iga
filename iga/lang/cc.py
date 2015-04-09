"""Build rules for C/C++."""

__all__ = [
    'init_cc',
]

import iga.env
from iga.argmatch import Oneof
from iga.label import Label
from iga.ninja import NinjaRule
from iga.path import PathGlob
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


def init_cc():
    """Init C/C++ build rules."""
    iga.env.register(NinjaRule.make(
        name=CC_COMPILE,
        command='$cc $cflags -c $in -o $out',
        description='CC $out',
    ))
    iga.env.register(NinjaRule.make(
        name=CC_LIBRARY,
        command='rm -f $out && $ar crs $out $in',
        description='AR $out',
    ))
    iga.env.register(NinjaRule.make(
        name=CC_BINARY,
        command='$cc $ldflags -o $out $in $libs',
        description='LINK $out',
    ))

    iga.env.register(RuleType.make(
        name=CC_LIBRARY,
        input_types=[CC_LIBRARY, CC_SOURCE],
        output_types=[CC_LIBRARY],
        #generate_buildstmts=generate_library,
    ))
    iga.env.register(RuleType.make(
        name=CC_BINARY,
        input_types=[CC_LIBRARY, CC_SOURCE],
        output_types=[CC_BINARY],
        #generate_buildstmts=generate_binary,
    ))

    iga.env.register(RuleFunc.make(cc_binary))
    iga.env.register(RuleFunc.make(cc_library))


def cc_library(
        name: Label,
        srcs: [Oneof(Label, PathGlob)]=(),
        deps: [Label]=()):
    return RuleData.make(
        type=CC_LIBRARY,
        name=name,
        inputs={
            CC_LIBRARY: deps,
            CC_SOURCE: srcs[Label],
        },
        inputs_patterns={
            CC_SOURCE: srcs[PathGlob],
        },
        outputs={
            CC_LIBRARY: [name.with_name(to_libname(name.name))],
        },
    )


def cc_binary(
        name: Label,
        srcs: [Oneof(Label, PathGlob)]=(),
        deps: [Label]=()):
    return RuleData.make(
        type=CC_BINARY,
        name=name,
        inputs={
            CC_LIBRARY: deps,
            CC_SOURCE: srcs[Label],
        },
        inputs_patterns={
            CC_SOURCE: srcs[PathGlob],
        },
        outputs={
            CC_BINARY: [name],
        },
    )


def to_libname(name):
    """X -> libX.a"""
    return 'lib%s.a' % name
