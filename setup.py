import subprocess
from setuptools import find_packages, setup

import iga


subprocess.check_call('./gen_manifest.sh')


setup(
    name = 'iga',
    version = iga.__version__,
    description = 'iga meta-build system',

    author = iga.__author__,
    author_email = iga.__author_email__,
    license = iga.__license__,
    url = 'https://github.com/clchiou/iga',

    packages = find_packages(exclude=['examples*', 'tests*']),
    scripts = ['bin/iga'],
)
