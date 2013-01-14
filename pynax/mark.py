"""
A mark is a line drawn over a view to mark a value.
"""
import types


class Mark:

    def __init__(self, axis, value, display_options={}):
        """
        """
        self.axis = axis
        self.value = value
        self.display_options = display_options

    def is_relative(self):
        return not isinstance(self.value, types.IntType)


def create_marks(axes, values, display_options=None):
    if len(axes) != len(values) or \
            (display_options is not None and
             len(axes) != len(display_options)):
        raise ValueError('All array counts must be the same' %
                         (len(axes), len(values)))
    if display_options is None:
        display_options == [{}] * len(axes)
    marks = []
    for axis, value, display_options_ in zip(axes, values, display_options):
        if display_options_ is None:
            display_options_ = {}
        marks.append(Mark(axis, value, display_options_))

    return tuple(marks)
