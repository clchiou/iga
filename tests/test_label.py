import unittest
from pathlib import PurePosixPath

from iga.error import IgaError
from iga.label import Label


class TestLabel(unittest.TestCase):

    def test_parse(self):
        package = 'a/b/c'

        self.assertEqual(
            make_label(package, 'd/e/f'),
            Label.parse('d/e/f', package),
        )
        self.assertEqual(
            make_label('x/y/z', 'd/e/f'),
            Label.parse('//x/y/z:d/e/f', package),
        )

        test_labels = [
            '//a/b/c:c',
            '//a/b/c:',
            '//a/b/c',
            ':c',
            'c',
        ]
        for label in test_labels:
            self.assertEqual(
                make_label(package, 'c'),
                Label.parse(label, package),
            )

    def test_error(self):
        package = 'a/b/c'
        illegal_labels = [
            '',
            ':',
            '//',
            '//:',
            '//:xyz',
        ]
        for label in illegal_labels:
            self.assertRaises(IgaError, Label.parse, label, package)


def make_label(package, target):
    return Label(PurePosixPath(package), PurePosixPath(target))


if __name__ == '__main__':
    unittest.main()
