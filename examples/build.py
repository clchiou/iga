from iga.main import main
from iga.workspace import workspace


workspace(
    source = 'src',
    variables = {
        'cxx': 'g++',
        'ar': 'ar',
        'cflags': '-I.',
    },
)

if __name__ == '__main__':
    main()
