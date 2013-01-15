from . import Figure, create_axes, Mark
from matplotlib import widgets


def show(*args):
    # Expand display_options if provided
    layers = []
    for arg in args:
        if isinstance(arg, tuple):
            layers.append((arg[0], arg[1]))
        else:
            layers.append((arg, {}))

    fig = Figure((2, 3))
    x, y, z, n = create_axes(['x', 'y', 'z', 'n'])
    mx = Mark(x, 20, {'color': 'r'})
    my = Mark(y, 20, {'color': 'g'})
    mz = Mark(z, 20, {'color': 'b'})
    mn = Mark(n, 20, {'color': 'k'})

    vx = fig.add((0, 2), layers[0][0], mx, y, z, [mn],
                 display_options=layers[0][1])
    vx.add_mark(my)
    vx.add_mark(mz)
    vy = fig.add((0, 1), layers[0][0], my, x, z, [mn],
                 display_options=layers[0][1])
    vy.add_mark(mx)
    vy.add_mark(mz)
    vz = fig.add((0, 0), layers[0][0], mz, x, y, [mn],
                 display_options=layers[0][1])
    vz.add_mark(mx)
    vz.add_mark(my)

    def update(val):
        if int(val) != mn.value:
            mn.value = int(val)
            fig.propagate_changes([mn])

    slider_ax = fig.get_subplot((1, 0), (3, 1))
    slider = widgets.Slider(slider_ax, 'n', 0, layers[0][0].shape[-1])
    slider.on_changed(update)
    """
    for data, options in layers[1:]:
        vx.add_layer(data, display_options=options)
        vy.add_layer(data, display_options=options)
        vz.add_layer(data, display_options=options)
    """
    return fig, slider
