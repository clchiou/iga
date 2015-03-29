__all__ = [
    'c_library',
    'c_program',
]

import itertools
import os.path

from iga.core import ImmutableOrderedSet
from iga.error import IgaError
from iga.label import FileLabel
from iga.label import ModuleLabel
from iga.label import glob
from iga.module import add_module
from iga.module import add_module_type
from iga.module import find_module
from iga.ninja import Buildstmt
from iga.ninja import add_rule


C_SOURCE = 'c_source'
C_OBJECT = 'c_object'
C_COMPILE = 'c_compile'
C_LIBRARY = 'c_library'
C_PROGRAM = 'c_program'


def init_c():
    add_rule(
        name=C_COMPILE,
        command='$cc $cflags -c $in -o $out',
        description='CC $out',
    )
    add_rule(
        name=C_LIBRARY,
        command='rm -f $out && $ar crs $out $in',
        description='AR $out',
    )
    add_rule(
        name=C_PROGRAM,
        command='$cc $ldflags -o $out $in $libs',
        description='LINK $out',
    )
    add_module_type(
        name=C_LIBRARY,
        input_types=[C_LIBRARY, C_SOURCE],
        output_types=[C_LIBRARY, C_OBJECT],
        generate_output_names=generate_output_names,
        generate_buildstmts=generate_library,
    )
    add_module_type(
        name=C_PROGRAM,
        input_types=[C_LIBRARY, C_SOURCE],
        output_types=[C_PROGRAM, C_OBJECT],
        generate_output_names=generate_output_names,
        generate_buildstmts=generate_program,
    )


def c_library(*, name, srcs, deps=()):
    if isinstance(srcs, str):
        srcs = (srcs,)
    if isinstance(deps, str):
        deps = (deps,)
    name = ModuleLabel.parse(name)
    add_module(
        type=C_LIBRARY,
        name=name,
        inputs={C_LIBRARY: [ModuleLabel.parse(dep) for dep in deps]},
        inputs_patterns={
            C_SOURCE: [glob(src) for src in srcs]
        },
        outputs={
            C_LIBRARY: [FileLabel.copy(name).replace(basename=to_libname)]
        },
    )


def c_program(*, name, srcs=(), deps=()):
    if isinstance(srcs, str):
        srcs = (srcs,)
    if isinstance(deps, str):
        deps = (deps,)
    if not srcs and not deps:
        raise IgaError('srcs and deps are empty')
    name = ModuleLabel.parse(name)
    add_module(
        type=C_PROGRAM,
        name=name,
        inputs={C_LIBRARY: [ModuleLabel.parse(dep) for dep in deps]},
        inputs_patterns={
            C_SOURCE: [glob(src) for src in srcs]
        },
        outputs={C_PROGRAM: [FileLabel.copy(name)]},
    )


def generate_output_names(inputs):
    return {C_OBJECT: [src.replace(ext='.o') for src in inputs[C_SOURCE]]}


def generate_objects(module, objs):
    assert module.type in (C_LIBRARY, C_PROGRAM)
    for obj, src in module.inputs.get(C_SOURCE, ()):
        obj = src.replace(ext='.o')
        objs.append(obj)
        yield Buildstmt.make(
            rule=C_COMPILE,
            outputs=[obj],
            explicit_deps=[src],
        )


def generate_library(module):
    assert module.type == C_LIBRARY
    objs = []
    yield from generate_objects(module, objs)
    libs = list(itertools.chain.from_iterable(
        find_module(lib).outputs.get(C_LIBRARY, ())
        for lib in module.inputs.get(C_LIBRARY, ())
    ))
    yield Buildstmt.make(
        rule=C_LIBRARY,
        outputs=module.outputs[C_LIBRARY],
        explicit_deps=objs,
        implicit_deps=libs,
    )


def generate_program(module):
    assert module.type == C_PROGRAM
    objs = []
    yield from generate_objects(module, objs)
    # Find transitive closure.
    libs = []
    queue = list(module.inputs.get(C_LIBRARY, ()))
    while queue:
        mod = find_module(queue.pop(0))
        libs.extend(mod.outputs.get(C_LIBRARY, ()))
        queue.extend(mod.inputs.get(C_LIBRARY, ()))
    lib_paths = ' '.join(ImmutableOrderedSet(
        '-L%s' % os.path.dirname(lib.relpath) for lib in libs
    ))
    lib_names = ' '.join(
        '-l%s' % from_libname(os.path.basename(lib.relpath)) for lib in libs
    )
    yield Buildstmt.make(
        rule=C_PROGRAM,
        outputs=module.outputs[C_PROGRAM],
        explicit_deps=objs,
        implicit_deps=libs,
        variables={'ldflags': lib_paths, 'libs': lib_names},
    )


def to_libname(name):
    """X -> libX.a"""
    return 'lib%s.a' % name


def from_libname(libname):
    """libX.a -> X"""
    assert libname.startswith('lib') and libname.endswith('.a')
    return libname[3:-2]


init_c()
