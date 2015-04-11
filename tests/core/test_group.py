import unittest

from iga.core import group


class TestGroup(unittest.TestCase):

    def test_group(self):
        self.assertEqual({'a': ['a', 'a'], 'b': ['b', 'b']}, group('abab'))
        self.assertEqual(
            {int: [1, 2], str: ['hello', 'world']},
            group([1, 'hello', 2, 'world'], key=type),
        )


if __name__ == '__main__':
    unittest.main()
