import unittest
from pathlib import Path

from iga.build_rules import glob_by_types
from iga.build_rules import is_not_empty
from iga.build_rules import update_pathlists
from iga.build_rules import update_pathsets
from iga.path import Glob


class TestHelpers(unittest.TestCase):

    def test_is_not_empty(self):
        self.assertFalse(is_not_empty({}))
        self.assertFalse(is_not_empty({'a': [], 'b': []}))
        self.assertTrue(is_not_empty({'a': ['x']}))
        self.assertTrue(is_not_empty({'a': ['x'], 'b': []}))

    def test_update_pathsets(self):
        psets = {'a': set(), 'b': set()}
        update_pathsets(psets, {'a': {1, 2, 3}})
        self.assertEqual({'a': {1, 2, 3}, 'b': set()}, psets)
        update_pathsets(psets, {'a': {2, 4}, 'b': {4, 5}})
        self.assertEqual({'a': {1, 2, 3, 4}, 'b': {4, 5}}, psets)

    def test_update_pathlists(self):
        plists = {'a': [], 'b': []}
        update_pathlists(plists, {'a': [1, 2, 3]})
        self.assertEqual({'a': [1, 2, 3], 'b': []}, plists)
        update_pathlists(plists, {'a': [1, 2, 3]})
        self.assertEqual({'a': [1, 2, 3], 'b': []}, plists)
        update_pathlists(plists, {'a': [3, -1], 'b': [4, 1, 5]})
        self.assertEqual({'a': [1, 2, 3, -1], 'b': [4, 1, 5]}, plists)

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
