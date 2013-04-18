from nisl import datasets, utils
from pynax.core import Mark, Refresher
from pynax.view import ImshowView
import pylab as pl
import numpy as np

nyu = datasets.fetch_nyu_rest(n_subjects=1)
func = nyu.func[0]
niimg = utils.check_niimg(func)
fig = pl.figure(figsize=(8, 2))
data = niimg.get_data()[..., 0]
# Awesome example activation map : take whatever is > .6 max
data_act = np.ma.MaskedArray(data, mask=(data < .6 * np.max(data)))

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

# Marks
mx = Mark(20, {'color': 'r'})
my = Mark(20, {'color': 'g'})
mz = Mark(20, {'color': 'b'})

# Figure axis
ax_x = pl.subplot(131)
ax_y = pl.subplot(132)
ax_z = pl.subplot(133)

ax_x.axis('off')
ax_y.axis('off')
ax_z.axis('off')

# Views

vx = ImshowView(ax_x, data, [mx, 'h', '-v'], display_options)
vx.add_hmark(my)
vx.add_vmark(mz)

vy = ImshowView(ax_y, data, ['h', my, '-v'], display_options)
vy.add_hmark(mx)
vy.add_vmark(mz)

vz = ImshowView(ax_z, data, ['h', '-v', mz], display_options)
vz.add_hmark(mx)
vz.add_vmark(my)

act_display_options = {}
act_display_options['interpolation'] = 'nearest'
act_display_options['cmap'] = pl.cm.autumn

#vx.add_layer(data_act, display_options=act_display_options)
#vy.add_layer(data_act, display_options=act_display_options)
#vz.add_layer(data_act, display_options=act_display_options)

vx.draw()
vy.draw()
vz.draw()

# Must be after all init
r = Refresher(fig, [mx, my, mz])

pl.show()
