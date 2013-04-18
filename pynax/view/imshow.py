from ..core import View


class ImshowView(View):

    def draw(self):
        for image in self.artists:
            image.remove()
        self.artists = []
        for data, options in self.layers:
            data_ = data.view
            image = self.ax.imshow(data_, **options)
            self.artists.append(image)
