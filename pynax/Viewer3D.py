from . import Figure, create_axes, Mark
from matplotlib import pyplot as pl


def show(*args):
    # Expand display_options if provided
    layers = []
    for arg in args:
        if isinstance(arg, tuple):
            layers.append((arg[0], arg[1]))
        else:
            layers.append((arg, {}))

    fig = Figure((2, 3))

    x, y, z = create_axes(['x', 'y', 'z'])
    mx = Mark(x, 20)
    my = Mark(y, 20)
    mz = Mark(z, 20)
    vx = fig.add((1, 2), layers[0][0], mx, z, y, display_options=layers[0][1])
    vx.add_mark(my)
    vx.add_mark(mz)
    vy = fig.add((0, 2), layers[0][0], my, z, x, display_options=layers[0][1])
    vy.add_mark(mx)
    vy.add_mark(mz)
    vz = fig.add((0, 0), layers[0][0], mz, y, x, shape=(2, 2),
                 display_options=layers[0][1])
    vz.add_mark(mx)
    vz.add_mark(my)

    for data, options in layers[1:]:
        vx.add_layer(data, display_options=options)
        vy.add_layer(data, display_options=options)
        vz.add_layer(data, display_options=options)
