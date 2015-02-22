import unittest

import iga
from iga.label import Label


class TestLabel(unittest.TestCase):

    def test_label_string(self):
        # Legitimate label strings.
        expected_label_string = '//a/b/c:c@default'
        current_package = 'a/b/c'
        for test_label_string in (
                '//a/b/c:c@default',
                '//a/b/c:c',
                '//a/b/c:@default',
                '//a/b/c:',
                '//a/b/c@default',
                '//a/b/c',
                ':c@default',
                ':c',
                'c@default',
                'c'):
            label = Label.from_string(test_label_string)
            label_string = label.as_string(current_package)
            self.assertEqual(expected_label_string, label_string)
        # Both package and target are empty.
        self.assertRaises(iga.Error, Label.from_string, '')
        self.assertRaises(iga.Error, Label.from_string, ':')
        self.assertRaises(iga.Error, Label.from_string, ':@default')
        # Empty variant string.
        self.assertRaises(iga.Error, Label.from_string, ':@')
        self.assertRaises(iga.Error, Label.from_string, '//package:target@')
        self.assertRaises(iga.Error, Label.from_string, '//package@')
        self.assertRaises(iga.Error, Label.from_string, ':target@')
