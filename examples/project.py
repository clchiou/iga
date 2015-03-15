from iga.project import project


project(
    source = 'src',
    build = 'build',
    variables = {'cflags': '-Isrc'},
)
