import unittest

from iga.core import list_difference


class TestListDifference(unittest.TestCase):

    def test_test_difference(self):
        self.assertEqual([], list_difference([], []))

        self.assertEqual([], list_difference([], [1]))
        self.assertEqual([], list_difference([], [1, 2]))
        self.assertEqual([], list_difference([], [1, 2, 3]))

        self.assertEqual([1], list_difference([1], []))
        self.assertEqual([1, 2], list_difference([1, 2], []))
        self.assertEqual([1, 2, 3], list_difference([1, 2, 3], []))

        self.assertEqual([], list_difference([1], [1]))
        self.assertEqual([9], list_difference([1, 9], [1, 2]))
        self.assertEqual(
            [9, 10, 11], list_difference([1, 2, 9, 10, 11], [1, 2, 3])
        )


if __name__ == '__main__':
    unittest.main()
