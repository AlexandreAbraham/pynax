from nisl import datasets, utils
from pynax.core import Mark
from pynax.view import ImshowView, PlotView
import pylab as pl
import numpy as np


nyu = datasets.fetch_nyu_rest(n_subjects=1)
func = nyu.func[0]
niimg = utils.check_niimg(func)
fig = pl.figure(figsize=(17, 6))
data = niimg.get_data()

# Awesome example activation map : take whatever is > .6 max
data_act = np.ma.MaskedArray(data * 0.8, mask=(data < .5 * np.max(data)))

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

# Marks
mx = Mark(20, {'color': 'r'})
my = Mark(20, {'color': 'g'})
mz = Mark(20, {'color': 'b'})
mn = Mark(0, {'color': 'k'})

# Figure axis
#ax_x = pl.subplot(231)
#ax_y = pl.subplot(232)
#ax_z = pl.subplot(233)
#ax_n = pl.subplot(212)

ax_x = fig.add_axes([0.0, 0.2, 0.37, 0.8])
ax_y = fig.add_axes([0.38, 0.2, 0.37, 0.8])
ax_z = fig.add_axes([0.76, 0.2, 0.23, 0.8])
ax_n = fig.add_axes([0.05, 0.05, 0.9, 0.195])

ax_x.axis('off')
ax_y.axis('off')
ax_z.axis('off')

# Views

vx = ImshowView(ax_x, data, [mx, 'h', '-v', mn], display_options)
vx.add_hmark(my)
vx.add_vmark(mz)

vy = ImshowView(ax_y, data, ['h', my, '-v', mn], display_options)
vy.add_hmark(mx)
vy.add_vmark(mz)

vz = ImshowView(ax_z, data, ['h', '-v', mz, mn], display_options)
vz.add_hmark(mx)
vz.add_vmark(my)

vn = PlotView(ax_n, data, [mx, my, mz, 'h'], {'color': 'gray'})
pl.ylim(0, np.max(data))
vn.add_hmark(mn)

ac_display_options = {}
ac_display_options['interpolation'] = 'nearest'
ac_display_options['cmap'] = pl.cm.autumn


vx.add_layer(data_act, [mx, 'h', '-v', mn], display_options=ac_display_options)
vy.add_layer(data_act, ['h', my, '-v', mn], display_options=ac_display_options)
vz.add_layer(data_act, ['h', '-v', mz, mn], display_options=ac_display_options)
vn.add_layer(data_act, [mx, my, mz, 'h'], display_options={'color': 'r'})

vx.draw()
vy.draw()
vz.draw()
vn.draw()

# Must be after all init
# r = Refresher(fig, [mx, my, mz, mn])

pl.show()
