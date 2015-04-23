"""File path utilities."""

__all__ = [
    'Glob',
]

import iga.fargparse


class Glob:
    """Keep a glob pattern before we have a Path object."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, path):
        return path.match(self.pattern)

    def glob(self, path):
        yield from path.glob(self.pattern)


def _parse(glob):
    if not isinstance(glob, Glob):
        raise iga.fargparse.ParseError()
    return glob


iga.fargparse.Parser.register_parse_func(Glob, _parse)
