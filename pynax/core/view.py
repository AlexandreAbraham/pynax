import numpy as np
import copy
from . import Data


class View(object):

    def __init__(self, ax, data, coord, display_options={}):
        self.data = Data(data, coord)
        self.hmarks = []
        self.vmarks = []
        # Suscribe to data update
        self.data.subscribe(self)
        self.layers = []
        self.add_layer(data, coord, copy.copy(display_options))

        # Used for display purpose
        self.ax = ax
        self.active = False
        self.active_x = None
        self.active_y = None
        self.artists = []
        self.background = None
        self.canvas = ax.figure.canvas
        self.canvas.mpl_connect('motion_notify_event',
                                self.motion_notify_event)
        self.canvas.mpl_connect('button_press_event',
                                self.button_press_event)
        self.canvas.mpl_connect('button_release_event',
                                self.button_release_event)
        self.canvas.mpl_connect('draw_event',
                                self._clear)

    def add_layer(self, data, coord, display_options):
        # XXX check data shape
        data = Data(data, coord)
        data.subscribe(self)
        self.layers.append((data, display_options))

    def add_vmark(self, mark):
        line = self.ax.axhline(mark.value, animated=True,
                               **mark.display_options)
        self.vmarks.append((mark, line))
        mark.subscribe(self)

    def add_hmark(self, mark):
        line = self.ax.axvline(mark.value, animated=True,
                               **mark.display_options)
        self.hmarks.append((mark, line))
        mark.subscribe(self)

    ###########################################################################
    # Display

    def draw(self):
        raise NotImplemented("A view must implement a draw() method")

    def _redraw_marks(self):
        if self.background is not None:
            self.canvas.restore_region(self.background)
        for _, line in self.hmarks:
            self.ax.draw_artist(line)
        for _, line in self.vmarks:
            self.ax.draw_artist(line)
        self.canvas.blit(self.ax.bbox)

    def _redraw(self):
        self.draw()
        self._redraw_marks()

    def _clear(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self._redraw_marks()

    def button_press_event(self, event):
        eventx, eventy = self.data.project(event.xdata, event.ydata)
        # Left mouse button
        if event.button != 1 or event.inaxes is None \
                or event.inaxes != self.ax:
            return
        self.active = True
        # Find closest marks
        if len(self.hmarks) != 0:
            dist = np.inf
            for x, l in self.hmarks:
                if abs(eventx - x.value) < dist:
                    dist = abs(eventx - x.value)
                    self.active_x = x, l
        if len(self.vmarks) != 0:
            dist = np.inf
            for y, l in self.vmarks:
                if abs(eventy - y.value) < dist:
                    dist = abs(eventy - y.value)
                    self.active_y = y, l

    def button_release_event(self, event):
        eventx, eventy = self.data.project(event.xdata, event.ydata)
        if self.active:
            self.motion_notify_event(event)
            self.active = False
            self.active_x = None
            self.active_y = None
        if event.button != 1 and event.inaxes == self.ax:
            pass
            # Get the value of the clicked pixel
            # data_ = self.layers[-1][0]
            # for mark_ in self.marks:
            #     data_ = data_[mark_.value]
            # data_ = data_[self.mark.value]
            # value = data_[event.ydata, event.xdata]
            # print value
            # for callback in self.callbacks:
            #     try:
            #         callback(self, value)
            #     except:
            #         continue

    def motion_notify_event(self, event):
        if not self.active or event.inaxes != self.ax:
            return
        eventx, eventy = self.data.project(event.xdata, event.ydata)
        if self.active_x is not None and \
                int(self.active_x[0].value) != int(eventx):
            self.active_x[0].update_value(int(eventx))
        if self.active_y is not None and \
                int(self.active_y[0].value) != int(eventy):
            self.active_y[0].update_value(int(eventy))

    def on_update(self, mark):
        redraw = False
        # If the mark is in the coord, we have to redraw the whole image
        # XXX we could store this information in the mark
        for data, _ in self.layers:
            if mark in data.coord:
                redraw = True
        for mark_ in self.hmarks:
            for hmark, line in self.hmarks:
                if mark == hmark:
                    val = self.data.project(mark.value, None)[0]
                    line.set_xdata((val, val))
        for mark_ in self.vmarks:
            for vmark, line in self.vmarks:
                if mark == vmark:
                    val = self.data.project(None, mark.value)[1]
                    line.set_ydata((val, val))
        if redraw:
            self._redraw()
        else:
            self._redraw_marks()
