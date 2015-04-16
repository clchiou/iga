import unittest

from iga.core import OrderedSet


class TestOrderedSet(unittest.TestCase):

    def test_contains(self):
        self.assertTrue('a' not in OrderedSet(''))
        self.assertTrue('a' in OrderedSet('a'))
        self.assertTrue('a' in OrderedSet('ba'))
        self.assertTrue('b' in OrderedSet('ba'))
        self.assertTrue('b' in OrderedSet('baaabc'))

    def test_order(self):
        self.assertEqual([], list(OrderedSet('')))
        self.assertEqual(list('a'), list(OrderedSet('a')))
        self.assertEqual(list('a'), list(OrderedSet('aa')))
        self.assertEqual(list('ab'), list(OrderedSet('aba')))
        self.assertEqual(list('ab'), list(OrderedSet('ababa')))

    def test_add_discard(self):
        oset = OrderedSet('')
        self.assertEqual([], list(oset))
        oset.add('b')
        oset.add('a')
        self.assertEqual(['b', 'a'], list(oset))
        oset.discard('b')
        self.assertEqual(['a'], list(oset))
        oset.discard('b')  # Do nothing when discard non-member.


if __name__ == '__main__':
    unittest.main()
