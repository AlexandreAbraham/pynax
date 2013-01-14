"""
A figure is a collection of views
"""
from matplotlib import pyplot as plt
from .view import View


class Figure:

    def __init__(self, grid):
        """
        XXX: Autoshape
        """
        self.grid = grid
        self.views = []
        self.fig = plt.figure()

    def add(self, position, data, mark, h_axis, v_axis,
            display_options={}, shape=(1, 1)):
        ax = plt.subplot2grid(self.grid, position,
                              colspan=shape[0], rowspan=shape[1])
        view = View(self, ax, data, mark, h_axis, v_axis,
                    display_options=display_options)
        self.fig.add_subplot(ax)
        self.views.append((view, ax))
        return view

    def show(self):
        self.fig.show()

    def propagate_changes(self, changes):
        for view, _ in self.views:
            view.propagate_changes(changes)
