"""Provides method for efficiently histogramming properties of events in a
region.
"""

# System imports
from uuid import uuid4
from array import array

# owls-parallel imports
from owls_parallel import parallelized

# owls-hep imports
from owls_hep.plotting import Plot, enable_fit

# Set up default exports
__all__ = [
    'plot',
    'plot2d',
]

# Dummy function to return fake values when parallelizing
def _plotting_mocker(*args, **kwargs):
    return

# Parallelization mapper batching on file path (i.e. one job per plot)
def _plotting_mapper(drawables, path, *args, **kwargs):
    return hash(path)

@parallelized(_plotting_mocker, _plotting_mapper, parallel_pass=2)
def plot(drawables_styles_options, path, *args, **kwargs):
    """Parallelized function to plot a list of 1D drawables with error bars.

    Args:
        obj: The list of objects (e.g. TH1F, TGraph, etc.) to plot
        path: The path to save the plot

    Recognized plotting options (and their default values):
        x_label: ''
        y_label: ''
        title: ''
        luminosity: None
        custom_label: ''
        atlas_label: ''
        extensions: ['pdf']
        enable_fit: None,
    """
    # Create a plot
    x_label = kwargs.get('x_label', '')
    y_label = kwargs.get('y_label', '')
    # TODO: Add support for log scale in the X-axis in owls_hep.plotting
    #x_log_scale = kwargs.get('x_log_scale', False)
    y_log_scale = kwargs.get('y_log_scale', False)
    title = kwargs.get('title', '')
    luminosity = kwargs.get('luminosity', None)
    custom_label = kwargs.get('custom_label', None)
    atlas_label = kwargs.get('atlas_label', None)
    extensions = kwargs.get('extensions', ['pdf'])
    fit = kwargs.get('enable_fit', None)

    # Create the plot
    plot = Plot(title, x_label, y_label)

    # Draw the histograms
    # Draw the object
    if fit is not None:
        enable_fit()
    plot.draw(*drawables_styles_options)
    enable_fit(False)

    # Set log scale
    # NOTE: This doesn't work. ROOT is stupid.
    #if y_log_scale:
        #plot.set_log_scale()

    # Draw a legend
    plot.draw_legend()

    # Draw an ATLAS stamp
    plot.draw_atlas_label(luminosity = luminosity,
                          custom_label = custom_label,
                          atlas_label = atlas_label)

    # Save
    plot.save(path, extensions)

@parallelized(_plotting_mocker, _plotting_mapper, parallel_pass=2)
def plot2d(drawable, path, *args, **kwargs):
    """Parallelized function to plot a 2D drawable

    Args:
        obj: The object (e.g. TH2F) to plot
        path: The path to save the plot

    Recognized plotting options (and their default values):
        x_label: ''
        y_label: ''
        title: ''
        options: 'COLZ'
    """
    # Create a plot
    x_label = kwargs.get('x_label', '')
    y_label = kwargs.get('y_label', '')
    title = kwargs.get('title', '')
    options = kwargs.get('options', 'COLZ')
    luminosity = kwargs.get('luminosity', None)
    custom_label = kwargs.get('custom_label', '')
    atlas_label = kwargs.get('atlas_label', '')
    extensions = kwargs.get('extensions', ['pdf'])

    # Create the plot
    plot = Plot(title, x_label, y_label)

    # Draw the object
    plot.draw((drawable, None, options))

    # Draw an ATLAS stamp
    plot.draw_atlas_label(luminosity = luminosity,
                          custom_label = custom_label,
                          atlas_label = atlas_label)

    # Save
    plot.save(path, extensions)
