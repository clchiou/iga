"""Context (variables) for interpreter."""

__all__ = [
    'make_context',
]

import iga.g
from . import core
from .core import as_dict
from .core import safe_update


def make_context():
    """Make a default Context object with __builtins__."""
    global_vars = as_dict(
        as_dict=core.as_dict,
        __builtins__=__builtins__,
    )
    return Context(global_vars, {})


class Context:
    """An exec() context."""

    def __init__(self, global_vars, local_vars):
        self.global_vars = global_vars
        self.local_vars = local_vars

    def copy(self):
        """Make a shallow copy of the context."""
        return Context(
            global_vars=dict(self.global_vars),
            local_vars=dict(self.local_vars),
        )

    def safe_update(self, dict_like):
        """Update local variables."""
        safe_update(self.local_vars, dict_like)
        return self

    def interpret(self, script_file, script_filename=None):
        """Interpret a script file in the context."""
        filename = getattr(script_file, 'name', script_filename)
        iga.g.log.debug('interpret "%s"', filename)
        code = compile(script_file.read(), filename, 'exec')
        exec(code, self.global_vars, self.local_vars)
