import unittest
from pathlib import PurePosixPath

from iga.path import Glob


class TestPath(unittest.TestCase):

    def test_glob(self):
        glob = Glob('**/foo.py')
        self.assertFalse(glob.match(PurePosixPath('foo.py')))
        self.assertTrue(glob.match(PurePosixPath('/foo.py')))
        self.assertTrue(glob.match(PurePosixPath('a/foo.py')))
        self.assertTrue(glob.match(PurePosixPath('a/b/foo.py')))
        self.assertTrue(glob.match(PurePosixPath('/a/b/foo.py')))


if __name__ == '__main__':
    unittest.main()
