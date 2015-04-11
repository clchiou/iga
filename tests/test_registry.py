import unittest
from collections import namedtuple

import iga.registry
from iga.registry import RegistryMixin
from iga.error import IgaError


class Foo(namedtuple('Foo', 'name'), RegistryMixin):
    pass


class Bar(Foo, RegistryMixin):
    pass


class TestRegistry(unittest.TestCase):

    def tearDown(self):
        iga.registry.reset()

    def test_registry(self):
        f = Foo('f')
        b = Bar('b')
        Foo.register(f)
        Bar.register(b)
        self.assertEqual({'f': f}, Foo.get_all_objects())
        self.assertEqual(f, Foo.get_object('f'))
        self.assertEqual({'b': b}, Bar.get_all_objects())
        self.assertEqual(b, Bar.get_object('b'))

        Foo.register(b)
        self.assertEqual({'f': f, 'b': b}, Foo.get_all_objects())
        self.assertEqual(b, Foo.get_object('b'))

        self.assertRaises(IgaError, Bar.register, f)

        self.assertRaises(KeyError, Bar.get_object, 'no-such-name')


if __name__ == '__main__':
    unittest.main()
