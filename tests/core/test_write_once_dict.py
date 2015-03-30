import unittest

from iga.core import WriteOnceDict


class TestWriteOnceDict(unittest.TestCase):

    def test_write_once(self):
        d = WriteOnceDict([(1, 1), (2, 2)])
        d[3] = 3
        self.assertEqual(3, len(d))
        self.assertEqual(1, d[1])
        self.assertEqual(2, d[2])
        self.assertEqual(3, d[3])
        self.assertEqual([1, 2, 3], sorted(d))
        self.assertRaises(KeyError, d.__setitem__, 1, 2)
        self.assertRaises(KeyError, d.__setitem__, 2, 3)
        self.assertRaises(KeyError, d.__delitem__, 1)
        self.assertRaises(KeyError, d.__delitem__, 2)


if __name__ == '__main__':
    unittest.main()
