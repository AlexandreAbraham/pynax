"""
"""
import numpy as np


class View:

    def __init__(self, fig, ax, data, mark, h_axis, v_axis,
                 display_options={}):
        """
        XXX: add display properties
        """
        # XXX: do value checking

        self.fig = fig
        self.ax = ax
        self.canvas = ax.figure.canvas
        # Create a convenient view for the data
        self.layers = []
        self.ims = []
        self.mark = mark
        self.h_axis = h_axis
        self.v_axis = v_axis
        self.h_marks = []
        self.v_marks = []
        self.active = False
        self.active_h = None
        self.active_v = None
        self.add_layer(data, display_options)
        ax.invert_yaxis()
        ax.axis('off')
        self.background = None
        self.canvas.mpl_connect('motion_notify_event',
                                self.motion_notify_event)
        self.canvas.mpl_connect('button_press_event',
                                self.button_press_event)
        self.canvas.mpl_connect('button_release_event',
                                self.button_release_event)
        self.canvas.mpl_connect('draw_event',
                                self.clear)

    def clear(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self._update()

    def add_layer(self, data, display_options={}):
        data = data.transpose([self.mark.axis.id,
                               self.h_axis.id,
                               self.v_axis.id])
        if len(self.layers) != 0:
            if self.layers[0][0].shape != data.shape:
                raise ValueError("All layers must have the same "
                                 "shape as the data")
        if not display_options.has_key('vmin'):
            display_options['vmin'] = np.min(data)
        if not display_options.has_key('vmax'):
            display_options['vmax'] = np.max(data)
        im = self.ax.imshow(data[self.mark.value], **display_options)
        self.layers.append((data, display_options))
        self.ims.append(im)

    def redraw_layers(self):
        # Remove all images
        for im in self.ims:
            im.remove()
        self.ims = []
        for data, options in self.layers:
            im = self.ax.imshow(data[self.mark.value], **options)
            self.ims.append(im)
        self.canvas.draw()
        self._update()

    def add_mark(self, mark):
        if mark.axis == self.h_axis:
            line = self.ax.axvline(self.ax.get_xbound()[0], animated=True)
            self.h_marks.append((mark, line))
        elif mark.axis == self.v_axis:
            line = self.ax.axhline(self.ax.get_ybound()[0], animated=True)
            self.v_marks.append((mark, line))
        else:
            raise ValueError('This mark does not correspond to any axis')

    def button_press_event(self, event):
        # Left mouse button
        if event.button != 1 or event.inaxes is None \
                or event.inaxes != self.ax:
            return
        self.active = True
        # Find closest marks
        if len(self.h_marks) != 0:
            dist = np.inf
            for h, l in self.h_marks:
                if abs(event.xdata - h.value) < dist:
                    dist = abs(event.xdata - h.value)
                    self.active_h = h, l
        if len(self.v_marks) != 0:
            dist = np.inf
            for v, l in self.v_marks:
                if abs(event.ydata - v.value) < dist:
                    dist = abs(event.ydata - v.value)
                    self.active_v = v, l

    def button_release_event(self, event):
        if self.active:
            self.active = False
            self.active_h = None
            self.active_v = None

    def motion_notify_event(self, event):
        if not self.active or event.inaxes != self.ax:
            return
        changes = []
        if self.active_h is not None and \
                int(self.active_h[0].value) != int(event.xdata):
            self.active_h[0].value = int(event.ydata)
            changes.append(self.active_h[0])
            self.active_h[1].set_xdata((event.xdata, event.xdata))
        if self.active_v is not None and \
                int(self.active_v[0].value) != int(event.ydata):
            self.active_v[0].value = int(event.xdata)
            changes.append(self.active_v[0])
            self.active_v[1].set_ydata((event.ydata, event.ydata))
        if len(changes) != 0:
            self._update()
            self.fig.propagate_changes(self, changes)

    def _update(self):
        if self.background is not None:
            self.canvas.restore_region(self.background)
        for _, line in self.h_marks:
            self.ax.draw_artist(line)
        for _, line in self.v_marks:
            self.ax.draw_artist(line)
        self.canvas.blit(self.ax.bbox)

    def propagate_changes(self, changes):
        for mark in changes:
            # Check main image
            if mark == self.mark:
                #self.im.remove()
                self.mark.value = mark.value
                #self.im = self.ax.imshow(self.data[mark.value],
                #                         **self.display_options)
                self.redraw_layers()
                #self.h_marks[0][1]._invalidy = True
           #else:
           #     for h_mark, _ in self.h_marks:
            #        if mark == h_mark:
