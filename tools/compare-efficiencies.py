#!/usr/bin/env python
# encoding: utf-8


# System imports
import argparse
from os import makedirs
from os.path import join, exists, isfile, dirname, basename
from array import array
from functools import partial
from uuid import uuid4

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.utility import load_file
from owls_hep.plotting import Plot
from owls_mutau.styling import standard_style

from ROOT import TLine, TF1, TGraph, TGraphAsymmErrors, gStyle

Plot.PLOT_LEGEND_LEFT = 0.60
Plot.PLOT_LEGEND_RIGHT = 1.0
Plot.PLOT_LEGEND_TEXT_SIZE = 0.035
Plot.PLOT_LEGEND_TEXT_SIZE_WITH_RATIO = 0.05
Plot.PLOT_LEGEND_ROW_SIZE = 0.07
Plot.PLOT_LEGEND_ROW_SIZE_WITH_RATIO = 0.10
Plot.PLOT_HEADER_HEIGHT = 300
Plot.PLOT_Y_AXIS_TITLE_OFFSET = 1.1
Plot.PLOT_Y_AXIS_TITLE_OFFSET_WITH_RATIO = 0.8

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Generate plots comparing efficiencies'
)
parser.add_argument('-o',
                    '--output',
                    default = 'plots/compare',
                    help = 'the output file name',
                    metavar = '<output>')
parser.add_argument('-f',
                    '--files',
                    nargs = '+',
                    help = 'files containing efficiencies')
parser.add_argument('-l',
                    '--labels',
                    nargs = '+',
                    help = 'labels representing the files '
                    '(must be as many as number of files)')
parser.add_argument('-t',
                    '--trigger',
                    default = 'tau25',
                    help = 'which trigger to compare')
parser.add_argument('-m',
                    '--mc',
                    default = False,
                    help = 'plot MC efficiencies (default: data)')
parser.add_argument('-x',
                    '--extensions',
                    nargs = '+',
                    default = ['pdf'],
                    help = 'save these extensions (default: pdf)')
parser.add_argument('--label',
                    nargs = '*',
                    help = 'items to add to the custom label',
                    metavar = '<items>')
parser.add_argument('definitions',
                    nargs = '*',
                    help = 'definitions to use within modules in the form x=y',
                    metavar = '<definition>')
arguments = parser.parse_args()


# Parse definitions
definitions = dict((d.split('=') for d in arguments.definitions))


if len(arguments.files) != len(arguments.labels):
    print('Mismatch between number of files and number of labels')
    print(arguments.files)
    print(arguments.labels)
    parser.print_help()
    exit(1)

for f in arguments.files:
    missing_file = False
    if not isfile(f):
        missing_file = True
        print('File {} is missing'.format(f))
    if missing_file:
        print('Exiting...')
        exit(1)

# Extract model parameters
try:
    luminosity = float(definitions['luminosity'])
except:
    luminosity = None
sqrt_s = float(definitions.get('sqrt_s', 13.0*1000*1000))


def plot_us(drawables, y_label, path, file_name, ratio=False,
            ratio_title='Ratio', limits=None):
    # Create the plot
    plot = Plot('',
                'p_{T}^{#tau} [GeV]',
                y_label,
                ratio = ratio)

    if limits is not None:
        for d in drawables:
            d.GetXaxis().SetLimits(*limits)

    # Compose the efficiencies and the fits
    styles = standard_style(count = len(drawables))
    draw_styles = ['ep' for d in drawables]
    drawables_styles_options = [
        (d, style, draw_style)
        for d, style, draw_style
        in zip(drawables, styles, draw_styles)
    ]
    legend_entries = drawables

    # Draw the main pad
    plot.draw(*drawables_styles_options)

    # TODO: Nothing here yet
    # if ratio:
        # # Draw the ratio pad
        # plot.draw_ratios(drawables_styles_options,
                         # y_range = (0.8, 1.2),
                         # y_title = ratio_title)

    # Draw a legend
    plot.draw_legend(legend_entries = legend_entries)

    # Draw an ATLAS stamp
    plot.draw_atlas_label(atlas_label = 'Internal',
                          sqrt_s = sqrt_s,
                          luminosity = luminosity,
                          custom_label = arguments.label
                         )

    # Save the plot
    save_path = join(path, file_name)
    plot.save(save_path, arguments.extensions)


# Create the directories for the different processes
base_path = dirname(arguments.output)
file_name = basename(arguments.output)
if not exists(base_path):
    makedirs(base_path)

print('Script options')
print('  Output directory: {}'.format(base_path))
print('  Files and labels:')
for f,l in zip(arguments.files, arguments.labels):
    print('    {} ⇒ {}'.format(l, f))

# Compare efficiencies
data_or_mc = ('mc' if arguments.mc else 'data')
file_objects = [load_file(f) for f in arguments.files]
efficiencies = [o.Get('eff_{}_{}'.format(arguments.trigger, data_or_mc))
                for o in file_objects]
for e,l in zip(efficiencies, arguments.labels):
    e.SetTitle(l)

plot_us(efficiencies, 'Efficiency', base_path, file_name)
