import os
import os.path
import unittest

import iga.context
from iga.path import get_caller_path
from iga.path import get_package
from iga.path import to_relpath


class TestPath(unittest.TestCase):

    def tearDown(self):
        iga.context.get_context().clear()

    def test_get_caller_path(self):
        relpath = 'iga/path.py'
        path = get_caller_path(-1)
        self.assertTrue(path.endswith(relpath), (path, relpath))
        relpath = 'iga/tests/test_path.py'
        path = get_caller_path(0)
        self.assertTrue(path.endswith(relpath), (path, relpath))

    def test_get_package(self):
        source = '/path/to/project/src'
        package = 'pkg/path/to'
        path = '%s/%s/package.py' % (source, package)
        self.assertEqual(
            package, get_package(path, context={'source': source}))

    def test_get_package_with_context(self):
        source = '/path/to/project/src'
        package = 'pkg/path/to'
        path = '%s/%s/package.py' % (source, package)
        iga.context.get_context()['source'] = source
        self.assertEqual(package, get_package(path))

    def test_to_path(self):
        project_root = '/path/to/project'
        source = project_root + '/src'
        context = {
            'project_root': project_root,
            'source': source,
        }
        self.assertEqual('src/a/b/c', to_relpath('a/b/c', context=context))


if __name__ == '__main__':
    unittest.main()
