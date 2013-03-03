from pynax import Viewer3D
import pylab as pl
import numpy as np
import matplotlib
import nibabel

colorlist = []
for red in np.linspace(0., 1., num=3):
    for green in np.linspace(0., 1., num=3):
        for blue in np.linspace(0., 1., num=3):
            colorlist.append((red, green, blue))
colorlist = np.asarray(colorlist)

mask_img = nibabel.load('leuven_mask.nii.gz')
mask = mask_img.get_data().astype(bool)
data_masked = np.load('parcellation.npy').astype(int)
data_masked += 1
data = np.zeros(mask.shape, dtype=int)
data[mask] = data_masked

m = np.max(data) + 1
colors = np.asarray(colorlist)
cmap_vec = np.arange(m) % len(colors)
colors_vec = colors[cmap_vec]
cmap = matplotlib.colors.ListedColormap(colors_vec)

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = cmap

v = Viewer3D.show((data, display_options),
                  title='Demo')


def update_color(view, value):
    cmap_vec[value] = (cmap_vec[value] + 1) % len(colors)
    print '[',
    for i in cmap_vec:
        print '%d,' % i,
    print ']'
    colors_vec = colors[cmap_vec]
    cmap = matplotlib.colors.ListedColormap(colors_vec)
    for view, _ in v.views:
        view.layers[-1][1]['cmap'] = cmap
        view.redraw_layers()


for view, _ in v.views:
    view.add_callback(update_color)

pl.show()
