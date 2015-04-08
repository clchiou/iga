__all__ = [
    'load_package',
]

import logging

import iga.env


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def load_package(package):
    buildfile_path = iga.env.root()['source'] / package / 'BUILD'
    LOG.info('load %s', buildfile_path)
    with buildfile_path.open() as buildfile:
        code = buildfile.read()
    code = compile(code, str(buildfile_path), 'exec')
    rule_data = []
    with iga.env.enter_child_env() as child_env:
        child_env['package'] = package
        child_env['rule_data'] = rule_data
        exec(code, make_context())
    labels_rules = []
    # TODO...
    return labels_rules


def make_context():
    return dict(iga.env.root()['rule_makers'])
