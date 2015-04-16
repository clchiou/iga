import unittest

from iga.core import KeyedSets


class TestKeyedSets(unittest.TestCase):

    def test_emptiness(self):
        ksets = KeyedSets(['a', 'b'])
        self.assertFalse(ksets)
        ksets['a'].add('x')
        self.assertTrue(ksets)

    def test_getitem(self):
        ksets = KeyedSets(['a', 'b'])
        self.assertRaises(KeyError, ksets.__getitem__, 'c')

    def test_ior(self):
        ksets = KeyedSets(['a', 'b'])
        ksets.update({'a': {1, 2, 3}, 'c': {4, 5, 6}})
        self.assertEqual({'a': {1, 2, 3}, 'b': set()}, ksets.as_dict_of_sets())
        ksets.update({'a': {2, 4}, 'b': {4, 5}})
        self.assertEqual(
            {'a': {1, 2, 3, 4}, 'b': {4, 5}}, ksets.as_dict_of_sets()
        )


if __name__ == '__main__':
    unittest.main()
