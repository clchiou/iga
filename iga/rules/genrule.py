"""Generate files with bash commands."""

__all__ = [
    'init',
]

import iga.filetype
from iga.core import group
from iga.fargparse import oneof
from iga.label import Label
from iga.ninja import NinjaBuildstmt
from iga.ninja import NinjaRule
from iga.path import Glob
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
    cmd = rule.variables['cmd']
    # TODO: $(location label) substitution on cmd.
    yield NinjaBuildstmt.make(
        ninja_rule=GENRULE,
        outputs=list(rule.outputs.all_values()),
        explicit_deps=list(rule.inputs.all_values()),
        variables={'cmd': cmd},
    )
