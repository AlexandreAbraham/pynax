from nisl import datasets, utils
from pynax import Viewer4D
import pylab as pl

nyu = datasets.fetch_nyu_rest(n_subjects=1)
func = nyu.func[0]
niimg = utils.check_niimg(func)
data = niimg.get_data()
# Awesome example activation map : take whatever is > .6 max
# data_act = np.ma.MaskedArray(data, mask=(data < .6 * np.max(data)))

display_options = {}
display_options['interpolation'] = 'nearest'
display_options['cmap'] = pl.cm.gray

act_display_options = {}
act_display_options['interpolation'] = 'nearest'
act_display_options['cmap'] = pl.cm.autumn

i = Viewer4D.show((data, display_options))

pl.show()
