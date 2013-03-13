"""Example usage of plot_roi(), on synthetic data."""

from enthought.mayavi import mlab
import numpy as np
import pynax


def ball_mask(size=(80, 80, 70)):
    """Create a boolean array containing a ball of "True"
    """
    g = np.mgrid[:size[0], :size[1], :size[2]].astype(np.float)
    for n in xrange(len(size)):
        g[n] -= size[n] / 2.
        g[n] /= (min(size) - 1)
    return (g * g).sum(axis=0) < 0.20


def inplace_lowpass_filter_3D(arr):
    """Simple low-pass filter.

    This function exists to avoid depending on scipy.
    """
    arr[1:, :, :] = (arr[:-1, :, :] + arr[1:, :, :]) / 2
    arr[:-1, :, :] = (arr[:-1, :, :] + arr[1:, :, :]) / 2

    arr[:, 1:, :] = (arr[:, :-1, :] + arr[:, 1:, :]) / 2
    arr[:, :-1, :] = (arr[:, :-1, :] + arr[:, 1:, :]) / 2

    arr[:, :, 1:] = (arr[:, :, :-1] + arr[:, :, 1:]) / 2
    arr[:, :, :-1] = (arr[:, :, :-1] + arr[:, :, 1:]) / 2


def generate_dataset():
    """Generate an partition of a ball.

    The partition is created by quantization of a filtered
    gaussian noise. Filtering is required to create regions
    not only composed of scattered points.
    """
    mask = ball_mask()
    # np.around
    cnum = 50.
    b = np.random.randn(*mask.shape)

    for n in xrange(100):
        inplace_lowpass_filter_3D(b)
    b = abs(b)
    b /= b[mask].max() / (cnum - 1)
    b = np.around(b).astype(np.int) + 1
    b[mask == False] = 0
    return b


if __name__ == "__main__":
    b = generate_dataset()
    pynax.plot_roi(b, (1, 40))
    mlab.show()
