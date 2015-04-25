"""Generate files with bash commands."""

__all__ = [
    'init',
]

import re

import iga.context
import iga.filetype
import iga.precond
from iga.core import group
from iga.fargparse import oneof
from iga.label import Label
from iga.ninja import NinjaBuildstmt
from iga.ninja import NinjaRule
from iga.path import Glob
from iga.rule import Rule
from iga.rule import RuleData
from iga.rule import RuleFunc
from iga.rule import RuleType


GENRULE = 'genrule'


def init():
    NinjaRule.register(NinjaRule.make(
        name=GENRULE,
        command='$cmd',
        description='GEN $out',
    ))

    RuleType.register(RuleType.make(
        name=GENRULE,
        input_types=RuleType.ANY_FILE_TYPE,
        output_types=RuleType.ANY_FILE_TYPE,
        ninja_rules=[GENRULE],
        generate_buildstmts=generate_genrule,
    ))

    RuleFunc.register(RuleFunc.make(genrule))


def genrule(
        name: Label,
        outs: [Label],
        cmd: str,
        srcs: [oneof(Label, Glob)]=()):
    srcs = group(srcs, key=type, as_dict=False)
    inputs = group(srcs[Label], key=iga.filetype.get, as_dict=False)
    input_patterns = srcs[Glob]
    outputs = group(outs, key=iga.filetype.get, as_dict=False)
    return RuleData.make(
        rule_type=GENRULE,
        name=name,
        inputs=inputs,
        input_patterns=input_patterns,
        outputs=outputs,
        variables={'cmd': cmd},
    )


def generate_genrule(rule):
    cmd = substitute(rule.variables['cmd'])
    yield NinjaBuildstmt.make(
        ninja_rule=GENRULE,
        outputs=list(rule.outputs.all_values()),
        explicit_deps=list(rule.inputs.all_values()),
        variables={'cmd': cmd},
    )


LITERAL = 'LITERAL'
SUBSTITUTION = 'SUBSTITUTION'


def substitute(string):
    pieces = []
    for kind, token in tokenize(string):
        if kind == LITERAL:
            pieces.append(token)
        elif kind == SUBSTITUTION:
            pieces.append(str(eval_substitution(token)))
        else:
            raise AssertionError('Unknown token kind %r' % kind)
    return ''.join(pieces)


def tokenize(string):
    if not string:  # Special case for empty string.
        yield (LITERAL, '')
    pattern = re.compile(r'\$(?P<LITERAL>\$)|\$\((?P<SUBSTITUTION>.*?)\)')
    pos = 0
    while True:
        match = pattern.search(string, pos=pos)
        if match is None:
            break
        if pos < match.start():
            yield (LITERAL, string[pos:match.start()])
        yield (match.lastgroup, match.group(match.lastindex))
        pos = match.end()
    literal = string[pos:]
    if literal:
        yield (LITERAL, literal)


def eval_substitution(string, *, _cxt=None):
    cxt = _cxt or iga.context.current()

    match = re.fullmatch(r'\s*location\s(.*)', string)
    if match:
        label = Label.parse_buildfile(match.group(1).strip())
        try:
            rule = Rule.get_object(label)
        except KeyError:
            return label.path
        rule_outputs = list(rule.outputs.all_values())
        iga.precond.check(
            1 == len(rule_outputs),
            'More than one outputs %r of rule %r', rule_outputs, label
        )
        return rule_outputs[0].path

    return cxt['variables'][string.strip()]
