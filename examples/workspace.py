import iga


iga.workspace(
    source = 'src',
    variables = {
        'cxx': 'g++',
        'ar': 'ar',
        'cflags': '-Isrc',
    },
)
