import unittest

from iga.core import ImmutableOrderedSet


class TestImmutableOrderedSet(unittest.TestCase):

    def test_contains(self):
        self.assertTrue('a' not in ImmutableOrderedSet(''))
        self.assertTrue('a' in ImmutableOrderedSet('a'))
        self.assertTrue('a' in ImmutableOrderedSet('ba'))
        self.assertTrue('b' in ImmutableOrderedSet('ba'))
        self.assertTrue('b' in ImmutableOrderedSet('baaabc'))

    def test_order(self):
        self.assertEqual([], list(ImmutableOrderedSet('')))
        self.assertEqual(list('a'), list(ImmutableOrderedSet('a')))
        self.assertEqual(list('a'), list(ImmutableOrderedSet('aa')))
        self.assertEqual(list('ab'), list(ImmutableOrderedSet('aba')))
        self.assertEqual(list('ab'), list(ImmutableOrderedSet('ababa')))


if __name__ == '__main__':
    unittest.main()
