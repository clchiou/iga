import unittest

from iga.core import Bimap
from iga.core import WriteOnceBimap


class TestBimap(unittest.TestCase):

    def test_bimap(self):
        bimap = Bimap()
        bimap.update(a=1, b=2, c=3)
        self.assertEqual(1, bimap['a'])
        self.assertEqual(2, bimap['b'])
        self.assertEqual(3, bimap['c'])
        self.assertEqual('a', bimap.get_key(1))
        self.assertEqual('b', bimap.get_key(2))
        self.assertEqual('c', bimap.get_key(3))
        self.assertEqual(None, bimap.get_key(4))
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, bimap)
        self.assertEqual({1: 'a', 2: 'b', 3: 'c'}, bimap.inverse())

        bimap['c'] = 4
        self.assertEqual(4, bimap['c'])
        self.assertEqual(None, bimap.get_key(3))
        self.assertEqual('c', bimap.get_key(4))
        self.assertEqual({'a': 1, 'b': 2, 'c': 4}, bimap)
        self.assertEqual({1: 'a', 2: 'b', 4: 'c'}, bimap.inverse())

    def test_error(self):
        self.assertRaises(KeyError, Bimap, [(1, 1), (2, 1)])

        bimap = Bimap({1: 'b', 2: 'a'})
        self.assertRaises(KeyError, bimap.__setitem__, 3, 'a')

        self.assertEqual({1: 'b', 2: 'a'}, bimap)
        self.assertEqual({'a': 2, 'b': 1}, bimap.inverse())

    def test_write_once_bimap(self):
        wobimap = WriteOnceBimap({'a': 1})
        self.assertEqual({'a': 1}, wobimap)
        self.assertEqual({1: 'a'}, wobimap.inverse())
        self.assertRaises(KeyError, wobimap.__setitem__, 'a', 2)
        self.assertRaises(KeyError, wobimap.__delitem__, 'a')


if __name__ == '__main__':
    unittest.main()
