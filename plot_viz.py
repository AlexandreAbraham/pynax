from nisl import datasets, utils
from pynax import Figure, Mark, create_axes
import pylab as pl
import numpy as np

nyu = datasets.fetch_nyu_rest(n_subjects=1)
func = nyu.func[0]
niimg = utils.check_niimg(func)
fig = Figure((2, 3))
data = niimg.get_data()[..., 0]
# Awesome example activation map : take whatever is > .6 max
data_act = np.ma.MaskedArray(data, mask=(data < .6 * np.max(data)))

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

x, y, z = create_axes(['x', 'y', 'z'])
mx = Mark(x, 20)
my = Mark(y, 20)
mz = Mark(z, 20)
vx = fig.add((1, 2), data, mx, z, y, display_options=display_options)
vx.add_mark(my)
vx.add_mark(mz)
vy = fig.add((0, 2), data, my, z, x, display_options=display_options)
vy.add_mark(mx)
vy.add_mark(mz)
vz = fig.add((0, 0), data, mz, y, x, shape=(2, 2),
             display_options=display_options)
vz.add_mark(mx)
vz.add_mark(my)

act_display_options = {}
act_display_options['interpolation'] = 'nearest'
act_display_options['cmap'] = pl.cm.autumn

vx.add_layer(data_act, display_options=act_display_options)
vy.add_layer(data_act, display_options=act_display_options)
vz.add_layer(data_act, display_options=act_display_options)
pl.show()
