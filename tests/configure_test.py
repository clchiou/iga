import unittest

from iga import IgaError
from iga.configures import IgaConfigure
from iga.configures import PackageConfigure


class TestConfigure(unittest.TestCase):

    def test_iga_configure(self):
        iga_configure = IgaConfigure()

        self.assertRaises(IgaError, iga_configure.source_root)
        self.assertEqual('src', iga_configure.source_root('src'))
        self.assertEqual('src', iga_configure.source_root())
        self.assertRaises(AssertionError, iga_configure.source_root, 1)

        self.assertEqual('build', iga_configure.build_root())
        self.assertEqual('out', iga_configure.build_root('out'))
        self.assertRaises(AssertionError, iga_configure.build_root, None)

        env = {'cc': 'gcc'}
        self.assertRaises(KeyError, iga_configure.environment, 'env')
        self.assertEqual(env, iga_configure.environment('env', env))
        self.assertEqual(env, iga_configure.environment('env'))
        self.assertEqual({}, iga_configure.environment('env', {}))
        self.assertEqual({}, iga_configure.environment('default'))

    def test_package_configure(self):
        package_configure = PackageConfigure()
        self.assertEqual([], package_configure.rules)

        package_configure.c_binary(name='a')
        self.assertEqual([('a', 'c_binary')], package_configure.rules)

        package_configure.c_library(name='b')
        self.assertEqual(
            [('a', 'c_binary'), ('b', 'c_library')], package_configure.rules)
