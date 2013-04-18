from ..core import View


class PlotView(View):

    def draw(self):
        if self.background is None:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
            for data, options in self.layers:
                data_ = data.view
                lines = self.ax.plot(data_, animated=True, **options)
                self.artists.append(lines)
        else:
            self.canvas.restore_region(self.background)
            for lines, (data, options) in zip(self.artists, self.layers):
                data_ = data.view
                lines[0].set_ydata(data_)
            for lines in self.artists:
                self.ax.draw_artist(lines[0])
