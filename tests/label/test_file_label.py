import os
import os.path
import unittest

import iga.context
from iga.label import FileLabel


class TestFileLabel(unittest.TestCase):

    def tearDown(self):
        iga.context.get_context().clear()

    def test_replace(self):
        label = FileLabel('a/b/c', 'd/e/f.ext')
        self.assertEqual(
            FileLabel('a/b/c', 'd/e/f.ext'), label.replace())
        self.assertEqual(
            FileLabel('a/b/c', 'd/e/x'), label.replace(basename='x'))
        self.assertEqual(
            FileLabel('a/b/c', 'd/e/y'), label.replace(basename=lambda _: 'y'))
        self.assertEqual(
            FileLabel('a/b/c', 'd/e/f.other'), label.replace(ext='.other'))
        self.assertEqual(
            FileLabel('a/b/c', 'd/e/f.other'),
            label.replace(ext=lambda _: '.other'),
        )
        label = FileLabel('a/b/c', 'file.txt')
        self.assertEqual(
            FileLabel('a/b/c', 'x'), label.replace(basename='x'))
        self.assertEqual(
            FileLabel('a/b/c', 'file.json'), label.replace(ext='.json'))

    def test_relpath(self):
        project_root = '/path/to/project'
        source = project_root + '/src'
        iga.context.get_context().update(
            project_root=project_root,
            source=source,
        )
        label = FileLabel('a/b/c', 'd/e/f.ext')
        self.assertEqual('src/a/b/c/d/e/f.ext', label.relpath)


if __name__ == '__main__':
    unittest.main()
