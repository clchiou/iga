import unittest

from iga.core import IgaError
from iga.label import Label


class TestLabel(unittest.TestCase):

    def test_label_string(self):
        # Legitimate label strings.
        expected_label_string = '//a/b/c:c@*'
        current_package = 'a/b/c'
        for test_label_string in (
                '//a/b/c:c',
                '//a/b/c:',
                '//a/b/c',
                ':c',
                'c'):
            label = Label.from_string(test_label_string)
            label_string = label.as_string(current_package)
            self.assertEqual(expected_label_string, label_string)

        expected_label_string = '//d/e/f:f@default'
        current_package = 'd/e/f'
        for test_label_string in (
                '//d/e/f:f@default',
                '//d/e/f:@default',
                '//d/e/f@default',
                ':f@default',
                'f@default'):
            label = Label.from_string(test_label_string)
            label_string = label.as_string(current_package)
            self.assertEqual(expected_label_string, label_string)

        # Both package and target are empty.
        self.assertRaises(IgaError, Label.from_string, '')
        self.assertRaises(IgaError, Label.from_string, ':')
        self.assertRaises(IgaError, Label.from_string, ':@default')

        # Empty variant string.
        self.assertRaises(IgaError, Label.from_string, ':@')
        self.assertRaises(IgaError, Label.from_string, '//package:target@')
        self.assertRaises(IgaError, Label.from_string, '//package@')
        self.assertRaises(IgaError, Label.from_string, ':target@')
