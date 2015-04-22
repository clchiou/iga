import unittest
import re
from pathlib import Path

from iga.build_rules import glob_keyed_sets
from iga.build_rules import match_keyed_sets
from iga.core import KeyedSets
from iga.label import Label
from iga.path import Glob


class TestHelpers(unittest.TestCase):

    def test_glob_keyed_sets(self):
        srcdir = Path(__file__).parent / 'test-data/src'
        package = 'pkg1'

        def get_file_type(label):
            return {'': 't1', '.txt': 't2', '.json': 't3'}[label.suffix]

        result = glob_keyed_sets(
            ['t1', 't2', 't3'],
            [],
            srcdir,
            package,
            _get_file_type=get_file_type,
        )
        self.assertEqual(
            {'t1': set(), 't2': set(), 't3': set()},
            result.as_dict_of_sets(),
        )

        result = glob_keyed_sets(
            ['t1', 't2', 't3'],
            [
                Glob('**/no-such-file'),
                Glob('**/*.txt'),
                Glob('*.txt'),
                Glob('**/*.json'),
            ],
            srcdir,
            package,
            _get_file_type=get_file_type,
        )
        self.assertEqual(
            {
                't1': set(),
                't2': {
                    Label.make(package, 'a.txt'),
                },
                't3': {
                    Label.make(package, 'b.json'),
                },
            },
            result.as_dict_of_sets(),
        )

    def test_match_keyed_sets(self):
        pkg = 'a/b/c'
        ksets = KeyedSets(['t1', 't2'])
        ksets['t1'].update([
            Label.make(pkg, 'd/e/f1'),
            Label.make(pkg, 'd/e/f2'),
            Label.make(pkg, 'a.txt'),
            Label.make(pkg, 'b.json'),
        ])
        patterns = [Glob('**/f*'), Glob('*.txt')]
        result = match_keyed_sets(ksets, patterns)
        self.assertEqual(
            {
                't1': {
                    Label.make(pkg, 'd/e/f1'),
                    Label.make(pkg, 'd/e/f2'),
                    Label.make(pkg, 'a.txt'),
                },
                't2': set(),
            },
            result.as_dict_of_sets(),
        )


if __name__ == '__main__':
    unittest.main()
