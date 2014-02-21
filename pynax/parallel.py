import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


class ParallelCoordinatesPlot(object):

    def __init__(self, data, labels, colors=None):
        self.data = data
        host = host_subplot(111, axes_class=AA.Axes)
        #plt.subplots_adjust(right=0.75)

        plt.gca().set_frame_on(False)
        host.set_frame_on(False)
        xticks = np.arange(data.shape[1])
        host.set_xticks(xticks)
        host.set_xticklabels(labels)
        host.yaxis.set_visible(False)
        host.tick_params(axis='x', length=0)
        host.axis['top'].set_visible(False)
        host.axis['right'].set_visible(False)

        host.set_ylim(np.min(data[:, 0]) - 0.1, np.max(data[:, 0]) + 0.1)
        axes = [host]
        for i in range(1, data.shape[1]):
            ax = host.twinx()
            ax.set_ylim(np.min(data[:, i]), np.max(data[:, i]))
            ax.axis["right"] = ax.new_floating_axis(1, value=i)
            ax.axis["right"].set_axis_direction("left")
            axes.append(ax)
        else:
            ax.axis["right"].set_axis_direction("right")

        self.axes = axes
        self.colors = colors

    def draw(self):
        # We transform the data
        data_ = self.data.copy()
        inverted = self.axes[0].transData.inverted().transform

        for i in range(1, self.data.shape[1]):
            data_[:, i] = inverted(self.axes[i].transData.transform(
                np.c_[np.ones(self.data.shape[0]), self.data[:, i]]))[:, 1]

        self.axes[0].set_xlim(0, self.data.shape[1] - 0.99)
        for i, d in enumerate(data_):
            kwargs = {}
            if self.colors is not None:
                kwargs['color'] = self.colors[i]
            plt.plot(d, **kwargs)


if __name__ == '__main__':
    import random
    base = [0, 0, 5, 5, 2]
    scale = [1.5, 2., 1.0, 2., 2.]
    data = [[base[x] + random.uniform(0., 1.) * scale[x]
            for x in xrange(5)] for y in xrange(30)]
    colors = ['r'] * 30

    base = [3, 6, 0, 1, 3]
    scale = [1.5, 2., 2.5, 2., 2.]
    data.extend([[base[x] + random.uniform(0., 1.) * scale[x]
                 for x in xrange(5)] for y in xrange(30)])
    colors.extend(['b'] * 30)
    labels = ['oh', 'ah', 'eh', 'uh', 'ih']
    pcp = ParallelCoordinatesPlot(np.asarray(data), labels, colors=colors)
    pcp.draw()
    pl.show()
