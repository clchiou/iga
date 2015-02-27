"""A project is a collection of packages."""

__all__ = [
    'make_project',
]

import os.path

import iga.configures

from .configure import ConfigureProperty
from .configure import MetaConfigure
from .context import make_context
from .package import make_package


def make_project(project_file_path):
    """Make default a Project object from a PROJECT file."""
    project_root = os.path.abspath(os.path.dirname(project_file_path))
    project_configure = make_project_configure(project_root)
    context = make_context().safe_update(project_configure.get_accessors())
    with open(project_file_path, 'r') as project_file:
        context.interpret(project_file)
    return Project(project_configure)


class Project:
    """A project is a collection of packages."""

    PACKAGE_FILE_NAME = 'PACKAGE'

    def __init__(self, project_configure):
        self.project_configure = project_configure
        self.packages = {}

    def __getitem__(self, package_name):
        """Load or return cached a package object."""
        if package_name not in self.packages:
            self.load_package(package_name)
        return self.packages[package_name]

    def load_package(self, package_name):
        """Load a PACKAGE file."""
        package_file_path = self._get_package_file_path(package_name)
        with open(package_file_path, 'r') as package_file:
            package = self._make_package(package_name, package_file)
        self.packages[package_name] = package

    def _get_package_file_path(self, package_name):
        """Return PACKAGE file path."""
        return os.path.join(
            self.project_configure.project_root(),
            self.project_configure.source_root(),
            package_name,
            Project.PACKAGE_FILE_NAME,
        )

    def _make_package(self, package_name, package_file):
        """Make a package object."""
        configures = [
            cls()
            for cls in self.project_configure.configure_classes().values()
        ]
        context = make_context()
        for configure in configures:
            context.safe_update(configure.get_accessors())
        context.interpret(package_file)
        return make_package(
            package_name, self._iter_rules(package_name, configures))

    def _iter_rules(self, package_name, configures):
        """Iterate over rules."""
        for configure in configures:
            yield from configure.make_rules(package_name)


def make_project_configure(project_root):
    """Make a ProjectConfigure object with default values."""
    project_configure = ProjectConfigure()
    project_configure.project_root(project_root)
    project_configure.build_root('build')
    project_configure.environments('default', {})
    project_configure.configure_classes().update(
        cc=iga.configures.CcConfigure,
    )
    return project_configure


class ProjectConfigure(metaclass=MetaConfigure):
    """Project configure object."""

    project_root = ConfigureProperty(
        str, """Absolute path to the project root directory.""")

    source_root = ConfigureProperty(
        str, """Relative path to the source directory.
        """)

    build_root = ConfigureProperty(
        str, """Relative ath to the build directory.
        """)

    default_target = ConfigureProperty(
        str, """Default build target.""")

    environments = ConfigureProperty(
        (str, dict), """Build environments.""")

    configure_classes = ConfigureProperty(
        (str, type), """Configure classes.""")
