"""Project configure."""

__all__ = [
    'ProjectConfigure',
    'make_project',
]

from .configure import ConfigureProperty
from .configure import MetaConfigure
from . import rulesets


def make_project():
    """Make a ProjectConfigure object with default values."""
    project = ProjectConfigure()
    project.build_root('build')
    project.environment('default', {})
    project.ruleset('cc', rulesets.make_cc_ruleset)
    return project


class ProjectConfigure(metaclass=MetaConfigure):
    """Project configure object."""

    source_root = ConfigureProperty(
        str, """Path to the root directory of source code.""")

    build_root = ConfigureProperty(
        str, """Path to the build output directory.""")

    default_target = ConfigureProperty(
        str, """Default build target.""")

    environment = ConfigureProperty(
        (str, dict), """Build environments.""")

    ruleset = ConfigureProperty(
        (str, object), """Build rule sets.""")
