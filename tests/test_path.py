import os
import os.path
import unittest

import iga.context
from iga.path import get_caller_path
from iga.path import get_package


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


if __name__ == '__main__':
    unittest.main()
