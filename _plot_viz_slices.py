from nisl import datasets, utils
from pynax import Figure, Mark, create_axes
import pylab as pl
import numpy as np

nyu = datasets.fetch_nyu_rest(n_subjects=1)
func = nyu.func[0]
niimg = utils.check_niimg(func)
fig = Figure((2, 7))
data = niimg.get_data()[..., 0]
# Awesome example activation map : take whatever is > .6 max
data_act = np.ma.MaskedArray(data, mask=(data < .6 * np.max(data)))

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

x, y, z = create_axes(['x', 'y', 'z'])
mx = Mark(x, 20)

marks = []
slices = []
for i in range(10):
    mz = Mark(z, i * 3 + 3)
    marks.append(mz)
    slices.append(fig.add((i / 5, i % 5), data, mz, x, y,
                          display_options=display_options))

    vx = fig.add((0, 5), data, mx, y, z, shape=(2, 2),
             display_options=display_options)
for m in marks:
    vx.add_mark(m)

act_display_options = {}
act_display_options['interpolation'] = 'nearest'
act_display_options['cmap'] = pl.cm.autumn

vx.add_layer(data_act, display_options=act_display_options)
for v in slices:
    v.add_layer(data_act, display_options=act_display_options)

pl.show()
