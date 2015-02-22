'''Process label string.'''

__all__ = [
    'Label',
]

from collections import namedtuple

import iga


class Label(namedtuple('Label', 'package target variant')):
    '''Represent a label string.'''

    @staticmethod
    def from_string(label_string):
        '''Parse a label string.'''
        # Parse '//package' part.
        if label_string.startswith('//'):
            package_start = 2
            package_end = (_find_or_none(label_string, ':', package_start) or
                           _find_or_none(label_string, '@', package_start) or
                           len(label_string))
        else:
            package_start = package_end = 0
        # Parse ':target' part.
        if label_string[package_end:package_end+1] == ':':
            target_start = package_end + 1
        else:
            target_start = package_end
        target_end = (_find_or_none(label_string, '@', target_start) or
                      len(label_string))
        # Parse '@variant' part.
        if label_string[target_end:target_end+1] == '@':
            variant = label_string[target_end+1:]
        else:
            variant = iga.DEFAULT_VARIANT
        if not variant:
            raise iga.Error(
                'cannot have empty variant after "@" in "%s"' %
                label_string)
        # Consstruct a Label object.
        package = label_string[package_start:package_end]
        target = label_string[target_start:target_end]
        if not package and not target:
            raise iga.Error(
                'cannot have both package and target empty in label "%s"' %
                label_string)
        return Label(package=package, target=target, variant=variant)

    def as_string(self, current_package):
        '''Transform into a label string.'''
        package = self.package or current_package
        target = self.target or _default_target(package)
        return '//%s:%s@%s' % (package, target, self.variant)


def _find_or_none(string, substring, start):
    '''Find the start of the substring or return None.'''
    index = string.find(substring, start)
    return index if index != -1 else None


def _default_target(package):
    '''Return the default target from a package string.'''
    return package[package.rfind('/')+1:]
