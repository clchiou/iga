import unittest
from pathlib import Path

from iga.build_rules import glob_by_types
from iga.path import Glob


class TestHelpers(unittest.TestCase):

    def test_glob_by_type(self):
        dirpath = Path(__file__).parent / 'test-data'

        pathsets_by_types = glob_by_types(
            ['t1', 't2', 't3'],
            {},
            dirpath,
        )
        self.assertEqual(
            {'t1': set(), 't2': set(), 't3': set()},
            pathsets_by_types,
        )

        pathsets_by_types = glob_by_types(
            ['t1', 't2', 't3'],
            {
                't1': [Glob('**/no-such-file')],
                't2': [Glob('**/*.txt')],
                't3': [Glob('*.txt'), Glob('**/*.json')],
            },
            dirpath,
        )
        self.assertEqual(
            {
                't1': set(),
                't2': {
                    dirpath / 'a.txt'
                },
                't3': {
                    dirpath / 'a.txt',
                    dirpath / 'b.json',
                    dirpath / 'c/d.json',
                },
            },
            pathsets_by_types,
        )


if __name__ == '__main__':
    unittest.main()
