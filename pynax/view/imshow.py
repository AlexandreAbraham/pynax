from ..core import View


class ImshowView(View):

    def draw(self):
        if self.background is None:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
            for data, options in self.layers:
                data_ = data.view
                image = self.ax.matshow(data_, animated=True, **options)
                self.artists.append(image)
        else:
            for image, (data, options) in zip(self.artists, self.layers):
                data_ = data.view
                image.set_array(data_)
            for image in self.artists:
                self.ax.draw_artist(image)
