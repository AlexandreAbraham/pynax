from os.path import join
import matplotlib
#matplotlib.use('WX')

import pylab as pl
import nibabel
import numpy as np
from pynax.core import Mark
from pynax.view import MatshowView, ImshowView, PlotView
from nilearn.resampling import resample_img


path = join('data', 'cov')
cov_mat = np.load(join(path, 'model0_corr.npy'))[0]
maps_img = nibabel.load(join(path, 'model0_umaps.nii.gz'))
maps = np.rollaxis(maps_img.get_data(), 3)
maps = np.ma.masked_less_equal(maps, 0)
time_series = np.load(join(path, 'learn_time_series_0.npy'))[0].T
# bg = nibabel.load('/usr/share/data/fsl-mni152-templates/MNI152_T1_1mm.nii.gz')
bg = nibabel.load('bg.nii.gz')
bg = resample_img(bg, target_shape=maps_img.shape[:3],
        target_affine=maps_img.get_affine())
bg = bg.get_data()

# Check lengths
assert(cov_mat.ndim == 2)
assert(cov_mat.shape[0] == cov_mat.shape[1])

n_regions = cov_mat.shape[0]

assert(maps.shape[0] == n_regions)
assert(time_series.shape[0] == n_regions)


def b(a, b, c, d, v=0.01):
    return [a + v, b + v, c - v, d - v]

fig = pl.figure(figsize=(17, 8))
ax_series = fig.add_axes(b(0.47, 0.025, 0.51, 0.265))
ax_s1 = fig.add_axes(b(0.45, 0.65, 0.22, 0.3))
ax_f1 = fig.add_axes(b(.67, 0.65, 0.185, 0.3))
ax_t1 = fig.add_axes(b(.855, 0.65, 0.125, 0.3))
ax_s2 = fig.add_axes(b(0.45, 0.3, 0.22, 0.3))
ax_f2 = fig.add_axes(b(0.67, 0.3, 0.185, 0.3))
ax_t2 = fig.add_axes(b(0.855, 0.3, 0.125, 0.3))
ax_cov = fig.add_axes(b(0., 0.0, 0.45, 1.))

ax_t1.axis('off')
ax_f1.axis('off')
ax_s1.axis('off')
ax_t2.axis('off')
ax_f2.axis('off')
ax_s2.axis('off')
ax_cov.axis('off')

# Marks
cov1 = Mark(1, {'color': 'b'})
cov2 = Mark(0, {'color': 'r'})
mx1 = Mark(20, {'color': 'b'})
my1 = Mark(20, {'color': 'b'})
mz1 = Mark(20, {'color': 'b'})
mx2 = Mark(20, {'color': 'r'})
my2 = Mark(20, {'color': 'r'})
mz2 = Mark(20, {'color': 'r'})

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

ac_display_options = {}
ac_display_options['interpolation'] = 'nearest'
ac_display_options['cmap'] = pl.cm.autumn

vx1 = ImshowView(ax_s1, bg, [mx1, 'h', '-v'], display_options)
vx1.add_layer(maps, [cov1, mx1, 'h', '-v'], ac_display_options)
vx1.add_hmark(my1)
vx1.add_vmark(mz1)

vy1 = ImshowView(ax_f1, bg, ['h', my1, '-v'], display_options)
vy1.add_layer(maps, [cov1, 'h', my1, '-v'], ac_display_options)
vy1.add_hmark(mx1)
vy1.add_vmark(mz1)

vz1 = ImshowView(ax_t1, bg, ['h', '-v', mz1], display_options)
vz1.add_layer(maps, [cov1, 'h', '-v', mz1], ac_display_options)
vz1.add_hmark(mx1)
vz1.add_vmark(my1)

vx2 = ImshowView(ax_s2, bg, [mx2, 'h', '-v'], display_options)
vx2.add_layer(maps, [cov2, mx2, 'h', '-v'], ac_display_options)
vx2.add_hmark(my2)
vx2.add_vmark(mz2)

vy2 = ImshowView(ax_f2, bg, ['h', my2, '-v'], display_options)
vy2.add_layer(maps, [cov2, 'h', my2, '-v'], ac_display_options)
vy2.add_hmark(mx2)
vy2.add_vmark(mz2)

vz2 = ImshowView(ax_t2, bg, ['h', '-v', mz2], display_options)
vz2.add_layer(maps, [cov2, 'h', '-v', mz2], ac_display_options)
vz2.add_hmark(mx2)
vz2.add_vmark(my2)

cov_display_options = {}
cov_display_options['interpolation'] = 'nearest'
cov_display_options['cmap'] = pl.cm.RdBu
cov_display_options['vmax'] = 1.
cov_display_options['vmin'] = -1.

vcov = MatshowView(ax_cov, -cov_mat, ['h', 'v'], cov_display_options)
vcov.add_hmark(cov2)
vcov.add_vmark(cov1)

vseries = PlotView(ax_series, time_series, [cov1, 'h'], {'color': 'b'},
        autoscale=True)
ax_series.set_ylim(time_series.min(), time_series.max())
vseries.add_layer(time_series, [cov2, 'h'], {'color': 'r'})

vx1.draw()
vy1.draw()
vz1.draw()
vx2.draw()
vy2.draw()
vz2.draw()
vcov.draw()
vseries.draw()

pl.show()
