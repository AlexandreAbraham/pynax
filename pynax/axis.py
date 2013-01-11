"""
Axis
"""
from collections import namedtuple


Axis = namedtuple('Axis', 'id name')


def create_axes(names):
    axes = []
    for id, name in enumerate(names):
        axes.append(Axis(id, name))
    return tuple(axes)
