__all__ = [
    'add_suffix',
    'get',
]


import iga.registry


def add_suffix(file_type, suffix):
    iga.registry.get(__name__ + ':suffixes')[suffix] = file_type


def get(label):
    return iga.registry.get(__name__ + ':suffixes')[label.suffix]
