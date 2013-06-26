Pynax
=====

Minimal visualization toolkit for Python (Python n-axis).

Pynax:
* offers a user friendly interface to display your multidimensional data in
  Python through the matplotlib API
* brings native interactivity to your plots. Easy as pie !

Warnings
--------

Pynax uses matplotib animated mode. Therefore, you must ensure that all your
plotsa and matplotlib images have not been garbage collected to ensure interactivity.
If at some point Pynax shows a non-interactive figure, this is most likely because
one of your plot or image is no more in memory.

Pynax uses axis related method instead of general methods. So, if you 'draw' a
matrix, you cannot use pl.colorbar() to add a color bar to it. You have to
specify image and axis (please see pynax.view.colorbar_mixin for an example of
how to add a colorbar properly)

Pynax is dependant of some matplotlib mechanisms. For example, when displaying a
2D slice from multidimensional data, vmin and vmax are obviously calculated on the
slice. If you change the values of the displayed slice (say, for example, that
you have 3D data and that you show another slice), vmin and vmax will not be
recomputed. A good practice is to always define vmin and vmax in the display
options when plotting multidimensional data (this will become mandatory in a
near future).

Concepts
--------

Pynax uses some concepts above matplotlib ones (but close to) to represent
plots.

* Mark: a mark is simply a value shared between different plots. If, at some
  point, a mark is updated, then its value will be updated in all the plot where
  it appears. A mark has some intrisic properties, like color, that are used
  when the mark is drawn on a plot.

* View: this is a kind of matplotlib axis, with some enhancement like the
  ability to draw several layers. All axis functionalities are not available in
  the view, use a mixin (see pynax.view.colorbar_mixin) to add them easily.
