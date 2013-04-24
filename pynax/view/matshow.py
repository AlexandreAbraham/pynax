from ..core import View


class MatshowView(View):

    def draw(self):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        for data, options in self.layers:
            data_ = data.view
            image = self.ax.matshow(data_, animated=True, **options)
            self.artists.append(image)

    def refresh(self):
        for image, (data, options) in zip(self.artists, self.layers):
            data_ = data.view
            image.set_array(data_)
        for image in self.artists:
            self.ax.draw_artist(image)
