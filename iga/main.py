__all__ = [
    'main',
]

import logging
import sys

import iga.env


# Good for debugging
logging.basicConfig(level=logging.DEBUG)


def main(argv=None):
    argv = argv or sys.argv
    print(iga.env.root())
    return 0
