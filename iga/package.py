__all__ = [
    'load_package',
]

import logging
import os.path

import iga.context
import iga.path


LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def load_package(package):
    package_path = os.path.join(iga.path.to_relpath(package), 'package.py')
    LOG.info('load %r', package_path)
    with open(package_path) as package_file:
        code = package_file.read()
    code = compile(code, package_path, 'exec')
    with iga.context.new_context(package=package):
        exec(code, {})
