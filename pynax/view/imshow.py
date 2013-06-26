from ..core import View
from .colorbar_mixin import ColorbarMixin


class ImshowView(View, ColorbarMixin):

    def draw(self):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        for data, options in self.layers:
            data_ = data.view
            image = self.ax.imshow(data_, animated=True, **options)
            self.artists.append(image)

    def refresh(self):
        for image, (data, options) in zip(self.artists, self.layers):
            data_ = data.view
            image.set_array(data_)
        for image in self.artists:
            self.ax.draw_artist(image)
