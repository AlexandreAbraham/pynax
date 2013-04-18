from ..core import View


class PlotView(View):

    def draw(self):
        for lines in self.artists:
            for line in lines:
                line.remove()
        self.artists = []
        for data, options in self.layers:
            data_ = data.view
            lines = self.ax.plot(data_, **options)
            self.artists.append(lines)
