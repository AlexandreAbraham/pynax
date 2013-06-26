import pylab as pl


class ColorbarMixin(object):
    def colorbar(self, layer_index=0):
        pl.colorbar(self.artists[layer_index], ax=self.ax)
