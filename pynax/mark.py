"""
A mark is a line drawn over a view to mark a value.
"""
import types


class Mark:

    def __init__(self, axis, value):
        """
        XXX: Add display properties (color...)
        """
        self.axis = axis
        self.value = value

    def is_relative(self):
        return not isinstance(self.value, types.IntType)


def create_marks(axes, values):
    if len(axes) != len(values):
        raise ValueError('Axes count (%d) is different than values count' %
                         (len(axes), len(values)))
    marks = []
    for axis, value in zip(axes, values):
        marks.append(Mark(axis, value))

    return tuple(marks)
