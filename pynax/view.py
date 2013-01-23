"""
"""
import numpy as np


class View:

    def __init__(self, fig, ax, data, mark, x_axis, y_axis, marks=[],
                 display_options={}):
        """
        """
        # XXX: do value checking

        self.fig = fig
        self.ax = ax
        self.canvas = ax.figure.canvas
        # Create a convenient view for the data
        self.layers = []
        self.ims = []
        self.mark = mark
        self.marks = marks
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x_marks = []
        self.y_marks = []
        self.active = False
        self.active_x = None
        self.active_y = None
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
        # split options
        pl_options = {}
        pn_options = {}
        for k, v in display_options.items():
            if k.startswith('pynax'):
                pn_options[k] = v
            else:
                pl_options[k] = v

        axis_id = [mark.axis.id for mark in self.marks]
        data = data.transpose(axis_id + [self.mark.axis.id,
                                         self.y_axis.id,
                                         self.x_axis.id])
        if len(self.layers) != 0:
            if self.layers[0][0].shape != data.shape:
                raise ValueError("All layers must have the same "
                                 "shape as the data")
        if not 'vmin' in pl_options:
            pl_options['vmin'] = np.min(data)
        if not 'vmax' in pl_options:
            pl_options['vmax'] = np.max(data)
        data_ = data
        for mark_ in self.marks:
            data_ = data[mark_.value]

        im = self.ax.imshow(data_[self.mark.value], **pl_options)
        if 'pynax_colorbar' in pn_options \
                and pn_options['pynax_colorbar']:
            self.ax.figure.colorbar(im, ax=self.ax)
        self.layers.append((data, pl_options))
        self.ims.append(im)

    def redraw_layers(self):
        # Remove all images
        for im in self.ims:
            im.remove()
        self.ims = []
        for data, options in self.layers:
            data_ = data
            for mark_ in self.marks:
                data_ = data[mark_.value]
            im = self.ax.imshow(data_[self.mark.value], **options)
            self.ims.append(im)
        self.canvas.draw()
        self._update()

    def add_mark(self, mark):
        if mark.axis == self.x_axis:
            line = self.ax.axvline(mark.value, animated=True,
                                   **mark.display_options)
            self.x_marks.append((mark, line))
        elif mark.axis == self.y_axis:
            line = self.ax.axhline(mark.value, animated=True,
                                   **mark.display_options)
            self.y_marks.append((mark, line))
        else:
            raise ValueError('This mark does not correspond to any axis')

    def button_press_event(self, event):
        # Left mouse button
        if event.button != 1 or event.inaxes is None \
                or event.inaxes != self.ax:
            return
        self.active = True
        # Find closest marks
        if len(self.x_marks) != 0:
            dist = np.inf
            for x, l in self.x_marks:
                if abs(event.xdata - x.value) < dist:
                    dist = abs(event.xdata - x.value)
                    self.active_x = x, l
        if len(self.y_marks) != 0:
            dist = np.inf
            for y, l in self.y_marks:
                if abs(event.ydata - y.value) < dist:
                    dist = abs(event.ydata - y.value)
                    self.active_y = y, l

    def button_release_event(self, event):
        if self.active:
            self.motion_notify_event(event)
            self.active = False
            self.active_x = None
            self.active_y = None

    def motion_notify_event(self, event):
        if not self.active or event.inaxes != self.ax:
            return
        changes = []
        if self.active_x is not None and \
                int(self.active_x[0].value) != int(event.xdata):
            self.active_x[0].value = int(event.xdata)
            changes.append(self.active_x[0])
        if self.active_y is not None and \
                int(self.active_y[0].value) != int(event.ydata):
            self.active_y[0].value = int(event.ydata)
            changes.append(self.active_y[0])
        if len(changes) != 0:
            # propagate_changes will be called by the figure
            self.fig.propagate_changes(changes)

    def _update(self):
        if self.background is not None:
            self.canvas.restore_region(self.background)
        for _, line in self.x_marks:
            self.ax.draw_artist(line)
        for _, line in self.y_marks:
            self.ax.draw_artist(line)
        self.canvas.blit(self.ax.bbox)

    def propagate_changes(self, changes):
        redraw = False
        update = False
        for mark in changes:
            # Check main image
            if mark == self.mark:
                self.mark.value = mark.value
                redraw = True
            else:
                for mark_ in self.marks:
                    if mark.axis == mark_.axis:
                        mark_.value = mark.value
                        redraw = True
                if mark.axis == self.x_axis:
                    for x_mark, line in self.x_marks:
                        if mark == x_mark:
                            x_mark.value = mark.value
                            line.set_xdata((mark.value, mark.value))
                        update = True
                if mark.axis == self.y_axis:
                    for y_mark, line in self.y_marks:
                        if mark == y_mark:
                            y_mark.value = mark.value
                            line.set_ydata((mark.value, mark.value))
                            update = True
        if redraw:
            self.redraw_layers()
        elif update:
            self._update()
