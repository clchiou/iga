import unittest
from pathlib import PurePosixPath

from iga.path import Glob
from iga.path import get_caller_path


class TestPath(unittest.TestCase):

    def test_glob(self):
        glob = Glob('**/foo.py')
        self.assertFalse(glob.match(PurePosixPath('foo.py')))
        self.assertTrue(glob.match(PurePosixPath('/foo.py')))
        self.assertTrue(glob.match(PurePosixPath('a/foo.py')))
        self.assertTrue(glob.match(PurePosixPath('a/b/foo.py')))
        self.assertTrue(glob.match(PurePosixPath('/a/b/foo.py')))

    def test_get_caller_path(self):
        path = PurePosixPath(get_caller_path(-1))
        self.assertTrue(str(path).endswith('iga/iga/path.py'))
        path = get_caller_path(0)
        self.assertTrue(str(path).endswith('iga/tests/test_path.py'))


if __name__ == '__main__':
    unittest.main()
