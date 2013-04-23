from nisl import datasets, utils
from pynax.core import Mark
from pynax.view import ImshowView
import pylab as pl
import numpy as np

nyu = datasets.fetch_nyu_rest(n_subjects=1)
func = nyu.func[0]
niimg = utils.check_niimg(func)
fig = pl.figure(figsize=(17, 5))
data = niimg.get_data()[..., 0]

# Awesome example activation map : take whatever is > .6 max
data_act = np.ma.MaskedArray(data * 0.8, mask=(data < .5 * np.max(data)))

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

# Marks
mx = Mark(20, {'color': 'r'})
marks = []
views = []
for i in range(10):
    mz = Mark(i * 3 + 3, {'color': 'b'})
    marks.append(mz)
    ax = fig.add_axes([0.14 * (i % 5), 0.55 * (1 - i / 5), 0.13, 0.45])
    ax.axis('off')
    vz = ImshowView(ax, data, ['h', '-v', mz], display_options)
    views.append(vz)
    vz.add_hmark(mx)

# Main figure
ax_z = fig.add_axes([0.7, 0., 0.3, 1.])
ax_z.axis('off')
vx = ImshowView(ax_z, data, [mx, 'h', '-v'], display_options)
for m in marks:
    vx.add_vmark(m)

act_display_options = {}
act_display_options['interpolation'] = 'nearest'
act_display_options['cmap'] = pl.cm.autumn

'''
vx.add_layer(data_act, display_options=act_display_options)
for v in slices:
    v.add_layer(data_act, display_options=act_display_options)
'''

vx.draw()
for v in views:
    v.draw()

pl.show()
