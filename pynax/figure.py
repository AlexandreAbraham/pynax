"""
A figure is a collection of views
"""
from matplotlib import pyplot as plt
from .view import View


class Figure:

    def __init__(self, grid, title=None):
        """
        XXX: Autoshape
        """
        self.grid = grid
        self.views = []
        opt = {}
        if title is not None:
            opt['num'] = title
        self.fig = plt.figure(**opt)

    def add(self, position, data, mark, h_axis, v_axis, marks=[],
            display_options={}, shape=(1, 1)):
        ax = self.get_subplot(position, shape)
        view = View(self, ax, data, mark, h_axis, v_axis, marks,
                    display_options=display_options)
        self.fig.add_subplot(ax)
        self.views.append((view, ax))
        return view

    def get_subplot(self, position, shape=(1, 1)):
        ax = plt.subplot2grid(self.grid, position,
                              colspan=shape[0], rowspan=shape[1])
        return ax

    def show(self):
        self.fig.show()

    def propagate_changes(self, changes):
        for view, _ in self.views:
            view.propagate_changes(changes)
