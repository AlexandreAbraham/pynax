import numpy as np
from . import Mark, UpdateMixin


def extract_data(data, indices):
    # Sanity check
    if data.ndim != len(indices):
        raise ValueError('Data and indices are not aligned')

    # Indices are either:
    # - a value, then we take the corresponding slice
    # - a mark, then we take the slice corresponding to the value os the mark
    # - 'h' or 'v', we consider them as ellipsis and transpose resulting data
    #   if they are not in the right order. If only one of them is present, a
    #   1D array is returned

    indices_ = []
    transpose = None
    for i in indices:
        if isinstance(i, Mark):
            indices_.append(i.value)
            continue
        if isinstance(i, basestring):
            s = slice(None)
            if i[0] == '-':
                s = slice(None, None, -1)
                i = i[1]
            if i == 'h':
                if transpose is None:
                    transpose = True
                indices_.append(s)
                continue
            if i == 'v':
                if transpose is None:
                    transpose = False
                indices_.append(s)
                continue
            raise ValueError('%s is not a valid index' % i)
        # i is a value
        indices_.append(i)
    indices_ = tuple(indices_)
    data_ = np.atleast_2d(data[indices_])
    if transpose:
        data_ = data_.T
    return data_


class Data(UpdateMixin):

    def __init__(self, data, coord):
        self.data = data
        self.view = extract_data(data, coord)
        self.coord = coord
        self.h_index = None
        self.h_flip = False
        self.v_index = None
        self.v_flip = False
        for i, c in enumerate(coord):
            if isinstance(c, Mark):
                c.subscribe(self)
            if isinstance(c, basestring):
                flip = False
                if c[0] == '-':
                    flip = True
                    c = c[1:]
                if c[0] == 'h':
                    self.h_index = i
                    self.h_flip = flip
                if c[0] == 'v':
                    self.v_index = i
                    self.v_flip = flip

    def project(self, h, v):
        ''' Turn x and y coord of plot into coordinates in our matrix
        '''
        #if v is not None and h is not None and self.v_index < self.h_index:
        #    t = h
        #    h = v
        #    v = t

        if h is not None and self.h_flip:
            h = -h % self.data.shape[self.h_index]

        if v is not None and self.v_flip:
            v = -v % self.data.shape[self.v_index]

        return h, v

    def on_update(self, object):
        self.view = extract_data(self.data, self.coord)
        self.fire_update(object)

    def __getitem__(self, a, b):
        return self.view.__getitem__(a, b)
