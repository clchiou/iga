import unittest

from iga.core import IgaError
from iga.configure import ConfigureProperty
from iga.configure import MetaConfigure


class Configure(metaclass=MetaConfigure):

    def __init__(self):
        super().__init__()

    scalar_int = ConfigureProperty(int, 'docstring')
    scalar_str = ConfigureProperty(str, 'docstring')

    mapping = ConfigureProperty((str, int), 'docstring')

    repeated_scalar = ConfigureProperty([int], 'docstring')
    repeated_tuple = ConfigureProperty([tuple], 'docstring')
    repeated_dict = ConfigureProperty([dict], 'docstring')


class TestConfigure(unittest.TestCase):

    def test_configure_scalar(self):
        configure = Configure()

        self.assertRaises(IgaError, configure.scalar_int)
        self.assertRaises(IgaError, configure.scalar_str)

        self.assertRaises(AssertionError, configure.scalar_int, '')
        self.assertRaises(AssertionError, configure.scalar_str, 0)

        self.assertEqual(1, configure.scalar_int(1))
        self.assertEqual(1, configure.scalar_int())
        self.assertEqual(2, configure.scalar_int(2))
        self.assertEqual(2, configure.scalar_int())

        self.assertEqual('hello', configure.scalar_str('hello'))
        self.assertEqual('hello', configure.scalar_str())
        self.assertEqual('world', configure.scalar_str('world'))
        self.assertEqual('world', configure.scalar_str())

    def test_configure_mapping(self):
        configure = Configure()

        self.assertEqual({}, configure.mapping())
        self.assertRaises(AssertionError, configure.mapping, 1)
        self.assertRaises(KeyError, configure.mapping, 'key')
        self.assertRaises(AssertionError, configure.mapping, 'key', 'value')
        self.assertEqual(1, configure.mapping('key', 1))
        self.assertEqual(1, configure.mapping('key'))
        self.assertEqual({'key': 1}, configure.mapping())

    def test_configure_repeated_scalar(self):
        configure = Configure()

        self.assertEqual([], configure.repeated_scalar())
        self.assertEqual([1], configure.repeated_scalar(1))
        self.assertEqual([1, 2], configure.repeated_scalar(2))
        self.assertEqual([1, 2], configure.repeated_scalar())

    def test_configure_repeated_tuple(self):
        configure = Configure()

        self.assertEqual([], configure.repeated_tuple())
        self.assertEqual([(1,)], configure.repeated_tuple(1))
        self.assertEqual([(1,), (2, 3)], configure.repeated_tuple(2, 3))
        self.assertEqual([(1,), (2, 3)], configure.repeated_tuple())

    def test_configure_repeated_dict(self):
        configure = Configure()

        self.assertEqual([], configure.repeated_dict())
        self.assertEqual([{'x':1}], configure.repeated_dict(x=1))
        self.assertEqual(
            [{'x':1}, {'y':2, 'z':3}], configure.repeated_dict(y=2, z=3))
        self.assertEqual(
            [{'x':1}, {'y':2, 'z':3}], configure.repeated_dict())
