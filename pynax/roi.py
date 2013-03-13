try:
    from mayavi import mlab
    from tvtk.api import tvtk
except ImportError:
    from enthought.mayavi import mlab
    from enthought.tvtk.api import tvtk

import numpy as np


def plot_roi(brain, labels):
    """3D-plot of brain and ROI.

    This command plot a 3D representation of ROI for brain imaging.
    The first argument must contain a full-brain parcellation, the
    second gives the ROI to be plotted. The full brain is shown
    as a "ghost" shape, allowing to see where the ROI are localized.

    brain: 3D-array giving brain labeling. Each value must be a
       numerical label defining a roi (0 must be outside).
    labels: {int or list of int}
       labels of roi to be shown.
    """
    fig = mlab.gcf()
    mlab.clf()
    fig.scene.disable_render = True
    dataset = tvtk.ImageData(spacing=(1, 1, 1), origin=(0, 0, 0))
    dataset.cell_data.scalars = np.ravel(brain, order="F")
    dataset.cell_data.scalars.name = "full brain"
    dataset.dimensions = tuple([n + 1 for n in brain.shape])
    source = mlab.pipeline.add_dataset(dataset)

    # Full-brain ghost display
    mlab.pipeline.outline(source)
    threshold = mlab.pipeline.threshold(source, low=1)
    surface = mlab.pipeline.surface(threshold)
    surface.actor.property.opacity = 0.15
    surface.actor.mapper.scalar_visibility = False

    # Selected zones display
    if not hasattr(labels, "__iter__"):
        labels = [labels]

    colors = [(1., 0., 0.), (0., 1., 0.), (0., 0., 1.),
              (1., 1., 0.), (0., 1., 1.), (1., 0., 1.)]

    for n, sel in enumerate(labels):
        threshold = mlab.pipeline.threshold(source,
                                            low=sel - 0.5, up=sel)
        surface = mlab.pipeline.surface(threshold)
        surface.actor.mapper.scalar_visibility = False
        surface.actor.property.color = colors[n % 6]
        surface.actor.property.edge_visibility = True
        surface.actor.property.line_width = 0.5
        surface.actor.property.edge_color = tuple(
            [v * 0.8 for v in colors[n % 6]])

    fig.scene.disable_render = False
