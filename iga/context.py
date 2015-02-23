'''Context (variables) for interpreter.'''

__all__ = [
    'make_default_context',
]

import iga.g

# Module for interpreting configure file.
import iga.interpreter.builtins


def make_default_context():
    '''Make a default context with __builtins__.'''
    global_vars = {
        name: value for name, value in vars(iga.interpreter.builtins).items()
        if name in iga.interpreter.builtins.__all__
    }
    global_vars['__builtins__'] = __builtins__
    return Context(global_vars, {})


class Context:
    '''An exec() context.'''

    def __init__(self, global_vars, local_vars):
        self.global_vars = global_vars
        self.local_vars = local_vars

    def copy(self):
        '''Make a shallow copy of the context.'''
        return Context(
            global_vars=dict(self.global_vars),
            local_vars=dict(self.local_vars),
        )

    def update(self, dict_or_iterable):
        '''Update local variables.'''
        self.local_vars.update(dict_or_iterable)
        return self

    def interpret(self, script_file, script_filename=None):
        '''Interpret a script file in the context.'''
        try:
            filename = script_file.name
        except AttributeError:
            filename = script_filename
        iga.g.logger.debug('interpret "%s"', filename)
        code = compile(script_file.read(), filename, 'exec')
        exec(code, self.global_vars, self.local_vars)
