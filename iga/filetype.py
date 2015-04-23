__all__ = [
    'add_suffix',
    'get',
    'get_all',
]


import iga.registry


FILE_TYPE_NONE = 'none'


def add_suffix(file_type, suffix):
    assert file_type != FILE_TYPE_NONE
    iga.registry.get(__name__)[suffix] = file_type


def get(label):
    return iga.registry.get(__name__).get(label.suffix, FILE_TYPE_NONE)


def get_all():
    file_types = sorted(iga.registry.get(__name__).values())
    file_types.append(FILE_TYPE_NONE)
    return file_types
