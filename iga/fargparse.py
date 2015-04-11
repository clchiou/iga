"""Function arguments parser."""

__all__ = [
    'FuncArgsParser',
    'ParseError',
    'Parser',
    'listof',
    'oneof',
]

import inspect
from abc import ABCMeta, abstractmethod

from iga.error import IgaError
from iga.registry import RegistryMixin


def listof(klass_or_parser):
    return ListOf.make(klass_or_parser)


def oneof(*klasses_or_parseres):
    return OneOf.make(*klasses_or_parseres)


class ParseError(Exception):
    """Raised on syntax errors."""
    pass


def _make_name(klass):
    return '%s.%s' % (klass.__module__, klass.__qualname__)


class Parser(RegistryMixin, metaclass=ABCMeta):
    """The interface of parsers."""

    @staticmethod
    def register_parse_func(klass, parse_func):
        Parser.register_with_name(
            _make_name(klass),
            ForwardingParser(parse_func),
        )

    @staticmethod
    def get_parser(klass):
        return Parser.get_object(_make_name(klass))

    @staticmethod
    def from_annotation(anno):
        if isinstance(anno, Parser):
            return anno
        elif isinstance(anno, list):
            return ListOf(Parser.from_annotation(anno[0]))
        else:
            return Parser.get_parser(anno)

    @abstractmethod
    def parse(self, value):
        raise NotImplementedError


class ForwardingParser(Parser):
    """Delegate parse to a parse_func."""

    def __init__(self, parse_func):
        self.parse_func = parse_func

    def parse(self, value):
        return self.parse_func(value)


ANY = ForwardingParser(lambda value: value)


class FuncArgsParser(Parser):
    """Parser for functions with only positional and keyword-only arguments."""

    _PAR_KINDS = (
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.KEYWORD_ONLY,
    )

    @staticmethod
    def make(func):
        sig = inspect.signature(func)
        parsers = []
        for name, par in sig.parameters.items():
            if par.kind not in FuncArgsParser._PAR_KINDS:
                raise IgaError(
                    'do not accept this kind of parameter %r' % par.kind)
            if par.annotation is inspect.Parameter.empty:
                parser = ANY
            else:
                parser = Parser.from_annotation(par.annotation)
            parsers.append((name, parser))
        return FuncArgsParser(parsers)

    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, args_kwargs):
        args, kwargs = args_kwargs
        if len(self.parsers) < len(args):
            raise ParseError(
                'expect no more than %d pos args but get %d',
                len(self.parsers), len(args))
        parsed_args = tuple(
            parser.parse(arg) for (_, parser), arg in zip(self.parsers, args)
        )
        kwarg_parsers = dict(self.parsers[len(args):])
        parsed_kwargs = {}
        ignored = []
        for name, value in kwargs.items():
            parser = kwarg_parsers.get(name)
            if parser:
                parsed_kwargs[name] = parser.parse(value)
            else:
                ignored.append(name)
        return parsed_args, parsed_kwargs, sorted(ignored)


class ListOf(Parser):

    @staticmethod
    def make(klass_or_parser):
        if isinstance(klass_or_parser, Parser):
            parser = klass_or_parser
        else:
            parser = Parser.get_parser(klass_or_parser)
        return ListOf(parser)

    def __init__(self, parser):
        self.parser = parser

    def parse(self, values):
        return [self.parser.parse(value) for value in values]


class OneOf(Parser):

    @staticmethod
    def make(*klasses_or_parsers):
        parsers = []
        for klass_or_parser in klasses_or_parsers:
            if isinstance(klass_or_parser, Parser):
                parser = klass_or_parser
            else:
                parser = Parser.get_parser(klass_or_parser)
            parsers.append(parser)
        return OneOf(parsers)

    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, value):
        for parser in self.parsers:
            try:
                return parser.parse(value)
            except ParseError:
                pass
        raise ParseError('%r is not one of the given types' % value)
