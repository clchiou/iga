'''Create module-like namespaces for global variables.'''

import sys

__all__ = [
    'Namespace',
    'install',
]


class Namespace:
    '''Write-once namespace object.'''

    _NO_ATTRIBUTE = "'Namespace' object has no attribute '%s'"
    _OVERWRITE = "cannot overwrite attribute '%s'"

    def __init__(self):
        # Bypass Namespace.__setattr__().
        object.__setattr__(self, 'namespace', {})

    def __hasattr__(self, name):
        return name in self.namespace

    def __getattr__(self, name):
        try:
            return self.namespace[name]
        except KeyError:
            raise AttributeError(self._NO_ATTRIBUTE % name)

    def __setattr__(self, name, value):
        if name in self.namespace:
            raise AttributeError(self._OVERWRITE % name)
        self.namespace[name] = value

    def __delattr__(self, name):
        try:
            self.namespace.pop(name)
        except KeyError:
            raise AttributeError(self._NO_ATTRIBUTE % name)


def install(name):
    '''Install namespace to sys.modules.'''
    if hasattr(sys, '_getframe'):
        caller_frame = sys._getframe(1)
    else:
        try:
            raise Exception()
        except Exception:
            caller_frame = sys.exc_info()[2].tb_frame.f_back
    caller_name = caller_frame.f_globals['__name__']
    if caller_name == '__name__':
        if name.startswith('.'):
            module_name = name[1:]
        else:
            module_name = name
    else:
        if name.startswith('.'):
            caller_name = caller_name[:caller_name.rindex('.')]
            module_name = caller_name + name
        else:
            module_name = '%s.%s' % (caller_name, name)
    namespace = Namespace()
    sys.modules[module_name] = namespace
    return namespace
