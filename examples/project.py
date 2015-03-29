import iga


iga.project(
    source = 'src',
    build = 'build',
    variables = {'cflags': '-Isrc'},
)

if __name__ == '__main__':
    iga.main()
