import unittest

import iga.registry
from iga.error import IgaError
from iga.fargparse import *


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ParseError()


class TestFuncArgsParser(unittest.TestCase):

    def setUp(self):
        Parser.register_parse_func(int, parse_int)
        Parser.register_parse_func(str, str)

    def tearDown(self):
        iga.registry.reset()

    def test_parse(self):
        def foo(a: int): pass
        parser = FuncArgsParser.make(foo)
        args = ('100',)
        kwargs = {'c': 'nothing', 'b': 'spam'}
        self.assertEqual(((100,), {}, ['b', 'c']), parser.parse((args, kwargs)))
        args = ()
        kwargs = {'a': '999', 'b': 'do not care'}
        self.assertEqual(((), {'a': 999}, ['b']), parser.parse((args, kwargs)))

        def bar(a: listof(int), b: [int], c: [oneof(int, str)]): pass
        parser = FuncArgsParser.make(bar)
        args = (['1', '2', '3'], ['4', '5', '6'], ['7', 'hello', 'world'])
        kwargs = {}
        parsed_args = ([1, 2, 3], [4, 5, 6], [7, 'hello', 'world'])
        parsed_kwargs = {}
        ignored = []
        self.assertEqual(
            (parsed_args, parsed_kwargs, ignored),
            parser.parse((args, kwargs)),
        )
        args = ()
        kwargs = {
            'a': ['1', '2', '3'],
            'b': ['4', '5', '6'],
            'c': ['7', 'hello', 'world'],
            'd': 'do not care',
            'e': 'some string',
        }
        parsed_args = ()
        parsed_kwargs = {
            'a': [1, 2, 3],
            'b': [4, 5, 6],
            'c': [7, 'hello', 'world'],
        }
        ignored = ['d', 'e']
        self.assertEqual(
            (parsed_args, parsed_kwargs, ignored),
            parser.parse((args, kwargs)),
        )

    def test_any(self):
        def foo(x): pass
        parser = FuncArgsParser.make(foo)
        args = ('1',)
        kwargs = {}
        self.assertEqual((('1',), {}, []), parser.parse((args, kwargs)))
        args = ()
        kwargs = {'x': '1'}
        self.assertEqual(((), {'x': '1'}, []), parser.parse((args, kwargs)))

    def test_error(self):
        def foo(*args): pass
        def bar(**kwargs): pass
        self.assertRaises(IgaError, FuncArgsParser.make, foo)
        self.assertRaises(IgaError, FuncArgsParser.make, bar)

        def spam(a: bytes): pass
        self.assertRaises(KeyError, FuncArgsParser.make, spam)


if __name__ == '__main__':
    unittest.main()
