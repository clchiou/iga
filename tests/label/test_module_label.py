import os
import os.path
import unittest

from iga.error import IgaError
from iga.label import ModuleLabel


class TestModuleLabel(unittest.TestCase):

    def test_parse(self):
        package = 'a/b/c'
        self.assertEqual(
            ModuleLabel(package, 'd/e/f'),
            ModuleLabel.parse('d/e/f', package=package),
        )
        self.assertEqual(
            ModuleLabel('x/y/z', 'd/e/f'),
            ModuleLabel.parse('//x/y/z:d/e/f', package=package),
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
                ModuleLabel(package, 'c'),
                ModuleLabel.parse(label, package=package),
            )

        illegal_labels = [
            '',
            ':',
            '//',
            '//:',
            '//:xyz',
        ]
        for label in illegal_labels:
            self.assertRaises(
                IgaError, ModuleLabel.parse, label, package=package)


if __name__ == '__main__':
    unittest.main()
