from iga.lang.c import c_program


c_program(
    name = 'hello',
    deps = '//lib:hello',
    srcs = 'main.c',
)
