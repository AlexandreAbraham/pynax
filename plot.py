import sys
import nibabel
from pynax.core import Mark
from pynax.view import ImshowView, PlotView
import pylab as pl
import numpy as np


if len(sys.argv) != 2:
    print 'Usage: %s <file>' % sys.argv[0]

fig = pl.figure(figsize=(17, 6))
data = nibabel.load(sys.argv[1]).get_data()

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

# Marks
mx = Mark(20, {'color': 'r'})
my = Mark(20, {'color': 'g'})
mz = Mark(20, {'color': 'b'})
mn = Mark(0, {'color': 'k'})

ax_x = fig.add_axes([0.0, 0.4, 0.37, 0.6])
ax_y = fig.add_axes([0.38, 0.4, 0.37, 0.6])
ax_z = fig.add_axes([0.76, 0.4, 0.23, 0.6])
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
pl.ylim(np.min(data), 8000.)
vn.add_hmark(mn)

print np.max(data)

vx.draw()
vy.draw()
vz.draw()
vn.draw()

pl.show()
