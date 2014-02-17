import pylab as pl
import numpy as np
from matplotlib import cm
from matplotlib.pyplot import Line2D


def parallel_coordinates(data, ax=None, labels=None,
        linestyles=None, colors=None, cmap=None):
    """ Parallel coordinates plot

    Parameters:
    -----------
    data: numpy array (n_samples, n_coordinates)
        Data to plot.

    ax: matplotlib axis (optional)
        The axis where the PCP must be plotted

    labels: list of n_coordinates labels (optional)
        Labels of the coordinates.

    linestyles: list of n_samples matplotlib linestyles (optional)
        Linestyles for all samples

    colors: ndarray of floats or string (optional)
        If cmap is None, colors must be an array of matplotlib colors.
        Otherwise, colors indicates the color value for each sample. If
        strings are passed, they are considered as categories.

    cmap: matplotlib colormap (optional)
        If specified, sample lines are colored depending on the colors
        parameter values.
    """

    dims = data.shape[1]
    xticks = np.arange(dims)
    labels = xticks if labels is None else labels
    if ax is None:
        ax = pl.gca()
    pl.subplots_adjust(left=0.1, bottom=0.1, right=.8, top=0.95)
    axes = [pl.axes(bb, frameon=False, xticks=[]) for bb in
            ax.get_position().splitx(*np.linspace(0, 1, dims)[1:-1])]

    colors_ = colors
    if colors is not None and cmap is not None:
        if isinstance(colors[0], basestring):
            _, colors_ = np.unique(colors, return_inverse=True)
        colors_ = colors_.astype(float) - np.min(colors_)
        colors_ = colors_ / np.max(colors_)
        if isinstance(cmap, basestring):
            cmap = cm.get_cmap(cmap)
        colors_ = np.asarray(cmap(colors_))

    ax.set_frame_on(False)
    ax.set_xticklabels(labels)
    ax.set_xticks(xticks)
    ax.tick_params(axis='x', pad=10)
    ax.set_xlim(0, dims - 1)
    ax.yaxis.set_visible(False)

    # Calculate the limits on the data
    mins = np.nanmin(data, axis=0)
    maxs = np.nanmax(data, axis=0)
    ranges = maxs - mins

    # Normalize the data
    data_ = (data - mins) / ranges

    # Plot the data on all the subplots
    for i, ax_ in enumerate(axes):
        for dsi, d in enumerate(data_):
            kwargs = {}
            if linestyles is not None:
                kwargs['linestyle'] = linestyles[dsi]
            if colors is not None:
                kwargs['color'] = colors_[dsi]
            ax_.plot([i, i + 1], d[i:i + 2], **kwargs)
        ylabels = np.linspace(np.min(data[:, i]), np.max(data[:, i]),
                len(ax_.get_yticklabels()))
        ax_.set_yticklabels(['%.2f' % ylabel for ylabel in ylabels])
        ax_.axvline(i, color='k')
        ax_.set_xlim(i, i + 1)
        # Last iteration
        if i == dims - 2:
            # We clone the last axes to put yticks on the right
            tx_ = ax_.twinx()
            ylabels = np.linspace(np.min(data[:, i + 1]),
                    np.max(data[:, i + 1]),
                len(tx_.get_yticklabels()))
            tx_.set_yticklabels(['%.2f' % ylabel for ylabel in ylabels])
            # .99, magic !
            ax_.axvline(i + .99, color='k')
            tx_.set_xlim(i, i + 1)
            ax.add_artist(ax_)
    # Legend
    scolors, index = np.unique(colors, return_index=True)
    scolors_ = np.asarray(colors_)[index]
    pl.legend([Line2D((0, 1), (0, 0), color=sc_) for sc_ in scolors_], scolors,
            loc='upper left', bbox_to_anchor=(1.3, 1.))
    return ax


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
    parallel_coordinates(np.asarray(data), labels=labels, colors=colors)
    pl.show()
