__all__ = [
    'c_library',
    'c_program',
]

import itertools
import os.path

from iga.core import ImmutableOrderedSet
from iga.label import FileLabel
from iga.label import ModuleLabel
from iga.module import add_module
from iga.module import add_module_type
from iga.module import find_module
from iga.ninja import add_rule
from iga.ninja import make_buildstmt


C_SOURCE = 'c_source'
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
        input_types=[C_SOURCE, C_LIBRARY],
        output_types=[C_LIBRARY],
        generate_buildstmts=generate_buildstmts,
    )
    add_module_type(
        name=C_PROGRAM,
        input_types=[C_SOURCE, C_LIBRARY],
        output_types=[C_PROGRAM],
        generate_buildstmts=generate_buildstmts,
    )


def c_library(*, name, srcs, deps=()):
    name = ModuleLabel.parse(name)
    srcs = list(itertools.chain.from_iterable(map(FileLabel.expand, srcs)))
    libs = [ModuleLabel.parse(dep) for dep in deps]
    inputs = {C_SOURCE: srcs, C_LIBRARY: libs}
    lib = FileLabel.copy(name).replace(basename=to_libname)
    outputs = {C_LIBRARY: [lib]}
    add_module(type=C_LIBRARY, name=name, inputs=inputs, outputs=outputs)


def c_program(*, name, srcs=(), deps=()):
    assert srcs or deps
    name = ModuleLabel.parse(name)
    srcs = list(itertools.chain.from_iterable(map(FileLabel.expand, srcs)))
    libs = [ModuleLabel.parse(dep) for dep in deps]
    inputs = {C_SOURCE: srcs, C_LIBRARY: libs}
    outputs = {C_PROGRAM: [FileLabel.copy(name)]}
    add_module(type=C_PROGRAM, name=name, inputs=inputs, outputs=outputs)


def generate_buildstmts(module_type, module):
    assert module_type in (C_LIBRARY, C_PROGRAM)
    objs = []
    for src in module.inputs[C_SOURCE]:
        obj = src.replace(ext='.o')
        objs.append(obj)
        yield make_buildstmt(
            rule=C_COMPILE,
            outputs=[obj],
            explicit_deps=[src],
        )
    if module_type == C_LIBRARY:
        libs = list(itertools.chain.from_iterable(
            find_module(lib).outputs[C_LIBRARY]
            for lib in module.inputs[C_LIBRARY]
        ))
        yield make_buildstmt(
            rule=C_LIBRARY,
            outputs=module.outputs[C_LIBRARY],
            explicit_deps=objs,
            implicit_deps=libs,
        )
    else:  # module_type == C_PROGRAM:
        libs = []
        queue = list(module.inputs[C_LIBRARY])
        while queue:
            mod = find_module(queue.pop(0))
            libs.extend(mod.outputs[C_LIBRARY])
            queue.extend(mod.inputs[C_LIBRARY])
        lib_paths = ' '.join(ImmutableOrderedSet(
            '-L%s' % os.path.dirname(lib.relpath) for lib in libs
        ))
        lib_names = ' '.join(
            '-l%s' % from_libname(os.path.basename(lib.relpath))
            for lib in libs
        )
        yield make_buildstmt(
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
