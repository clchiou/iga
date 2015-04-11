__all__ = [
    'CustomMatcher',
    'KwargsMatcher',
    'MatchError',
    'listof',
    'oneof',
]

import inspect
from abc import ABCMeta, abstractmethod

from iga.core import WriteOnceDict
from iga.registry import RegistryMixin


def listof(klass_or_matcher):
    return ListOf.make(klass_or_matcher)


def oneof(klasses_or_matcheres):
    return OneOf.make(klasses_or_matcheres)


class MatchError(Exception):
    pass


class Matcher(RegistryMixin, metaclass=ABCMeta):

    @abstractmethod
    def match(self, value):
        raise NotImplementedError


class KwargsMatcher(Matcher):

    @staticmethod
    def parse(func, get_matcher=None):
        get_matcher = get_matcher or CustomMatcher.get_matcher
        signature = inspect.signature(func)
        matchers = WriteOnceDict()
        for par in signature.parameters:
            if par.annotation is not par.empty:
                matchers[par.name] = _parse(par.annotation, get_matcher)
        return KwargsMatcher(matchers)

    def __init__(self, matchers):
        self.matchers = matchers

    def match(self, kwargs):
        matched_kwargs = {}
        ignored = []
        for name, value in kwargs.items():
            matcher = self.matchers.get(name)
            if matcher:
                matched_kwargs[name] = matcher.match(value)
            else:
                ignored.append(name)
        return matched_kwargs, sorted(ignored)


def _parse(anno, get_matcher):
    if isinstance(anno, Matcher):
        return anno
    elif isinstance(anno, list):
        return ListOf(_parse(anno[0], get_matcher))
    else:
        return get_matcher(anno)


class ListOf(Matcher):

    @staticmethod
    def make(klass_or_matcher, get_matcher=None):
        get_matcher = get_matcher or CustomMatcher.get_matcher
        if isinstance(klass_or_matcher, Matcher):
            matcher = klass_or_matcher
        else:
            matcher = get_matcher(klass_or_matcher)
        return ListOf(matcher)

    def __init__(self, matcher):
        self.matcher = matcher

    def match(self, values):
        return [self.matcher.match(value) for value in values]


class OneOf(Matcher):

    @staticmethod
    def make(*klasses_or_matchers, get_matcher=None):
        get_matcher = get_matcher or CustomMatcher.get_matcher
        matchers = []
        for klass_or_matcher in klasses_or_matchers:
            if isinstance(klass_or_matcher, Matcher):
                matcher = klass_or_matcher
            else:
                matcher = get_matcher(klass_or_matcher)
            matchers.append(matcher)
        return OneOf(matchers)

    def __init__(self, matchers):
        self.matchers = matchers

    def match(self, value):
        for matcher in self.matchers:
            try:
                return matcher.match(value)
            except MatchError:
                pass
        raise MatchError('%r is not one of the given types' % value)


class Any(Matcher):

    def match(self, value):
        return value


ANY = Any()


class CustomMatcher(Matcher, RegistryMixin):

    @staticmethod
    def get_matcher(klass):
        try:
            return CustomMatcher.get_object(_make_name(klass))
        except KeyError:
            return ANY

    def __init__(self, klass, match_func):
        self.klass = klass
        self.match_func = match_func

    @property
    def name(self):
        return _make_name(self.klass)

    def match(self, value):
        return self.match_func(value)


def _make_name(klass):
    return '%s.%s' % (klass.__module__, klass.__qualname__)
