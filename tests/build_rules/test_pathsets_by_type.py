import unittest

from iga.build_rules import is_not_empty
from iga.build_rules import update_pathsets


class TestPathsetsByType(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
