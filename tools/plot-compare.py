#!/usr/bin/env python
# encoding: utf8


# System imports
import argparse
from os import makedirs
from os.path import join, exists, isdir
from itertools import product, chain
from math import sqrt
from copy import copy

# Six imports
from six import itervalues
from six.moves import range

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.plotting import Plot, combined_histogram, ratio_histogram
from owls_hep.utility import integral, get_bins_errors

# owls-mutau imports
from owls_mutau.styling import default_black, default_red

Plot.PLOT_HEADER_HEIGHT = 500
Plot.PLOT_LEGEND_LEFT = 0.50
Plot.PLOT_LEGEND_RIGHT = 0.95
Plot.PLOT_LEGEND_TEXT_SIZE = 0.05
Plot.PLOT_LEGEND_TEXT_SIZE_WITH_RATIO = 0.055
Plot.PLOT_LEGEND_ROW_SIZE = 0.06
Plot.PLOT_LEGEND_ROW_SIZE_WITH_RATIO = 0.065

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Generate plots and a combined plotbook'
)
parser.add_argument('-o',
                    '--output',
                    default = 'plots',
                    help = 'the plot output directory',
                    metavar = '<output>')
parser.add_argument('--model-file-1',
                    help = 'the path to the first model definition module to compare',
                    required = True,
                    metavar = '<model-file>')
parser.add_argument('--model-file-2',
                    help = 'the path to the second model definition module to compare',
                    required = True,
                    metavar = '<model-file>')
parser.add_argument('--data-prefix-1',
                    help = 'the data prefix of the first sample set ',
                    required = True,
                    metavar = '<path>')
parser.add_argument('--data-prefix-2',
                    help = 'the data prefix of the second sample set',
                    required = True,
                    metavar = '<path>')
parser.add_argument('-p',
                    '--processes',
                    nargs = '+',
                    help = 'the processes to plot',
                    metavar = '<process>')
parser.add_argument('--regions-file-1',
                    help = 'the path to the first region definition module to compare',
                    required = True,
                    metavar = '<regions-file>')
parser.add_argument('--regions-file-2',
                    help = 'the path to the second region definition module to compare',
                    required = True,
                    metavar = '<regions-file>')
parser.add_argument('--title-1',
                    help = 'the title of the first histogram',
                    required = True,
                    metavar = '<title>')
parser.add_argument('--title-2',
                    help = 'the title of the first histogram',
                    required = True,
                    metavar = '<title>')
parser.add_argument('-r',
                    '--regions',
                    nargs = '+',
                    help = 'the regions to plot',
                    metavar = '<region>')
parser.add_argument('-D',
                    '--distributions-file',
                    required = True,
                    help = 'the path to the histograms definition module',
                    metavar = '<distributions-file>')
parser.add_argument('-d',
                    '--distributions',
                    nargs = '+',
                    help = 'the histograms to plot',
                    metavar = '<distribution>')
parser.add_argument('-E',
                    '--environment-file',
                    required = True,
                    help = 'the path to the environment definition module',
                    metavar = '<environment-file>')
parser.add_argument('-t',
                    '--text-counts',
                    action = 'store_true',
                    help = 'enable text output of counts')
parser.add_argument('-n',
                    '--no-counts',
                    action = 'store_true',
                    help = 'disable event counts in legends')
parser.add_argument('--ratio-title',
                    help = 'Y-axis title to use for the ratio histogram',
                    metavar = '<ratio-title>')
parser.add_argument('-e',
                    '--error-label',
                    default = 'Stat. Unc.',
                    help = 'the label to use for error bands',
                    metavar = '<error-label>')
parser.add_argument('-l',
                    '--label',
                    nargs = '*',
                    help = 'items to add to the custom label',
                    metavar = '<items>')
parser.add_argument('-a',
                    '--atlas-label',
                    default = 'Internal',
                    help = 'the label to use for the ATLAS stamp',
                    metavar = '<atlas-label>')
parser.add_argument('-x',
                    '--extensions',
                    nargs = '+',
                    default = ['pdf'],
                    help = 'save these extensions (default: pdf)')
parser.add_argument('definitions',
                    nargs = '*',
                    help = 'definitions to use within modules in the form x=y',
                    metavar = '<definition>')
arguments = parser.parse_args()


# Parse definitions
definitions = dict((d.split('=') for d in arguments.definitions))
definitions1 = copy(definitions)
definitions1['data_prefix'] = arguments.data_prefix_1
definitions2 = copy(definitions)
definitions2['data_prefix'] = arguments.data_prefix_2

# Load files
model_file1 = load_module(arguments.model_file_1, definitions1)
model_file2 = load_module(arguments.model_file_2, definitions2)
regions_file1 = load_module(arguments.regions_file_1, definitions1)
regions_file2 = load_module(arguments.regions_file_2, definitions2)
distributions_file = load_module(arguments.distributions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)

# Get luminosity and energy
luminosity = model_file1.luminosity
sqrt_s = model_file1.sqrt_s

# Extract histogram distributions
distributions = dict((
    (d, getattr(distributions_file, d))
    for d
    in arguments.distributions
))

# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
backend = getattr(environment_file, 'parallelization_backend', None)

# Create the parallelization environment
parallel = ParallelizedEnvironment(backend)

# Create output directories
for region_name in arguments.regions:
    # Compute the region's output path
    region_path = join(arguments.output, region_name)

    # Try to create it
    if not exists(region_path):
        makedirs(region_path)


# Run in a cached environment
with caching_into(cache):
    # Run in a parallelized environment
    while parallel.run():
        if parallel.computed():
            print('Creating plots...')

        # Loop over regions and distributions
        for region_name, distribution_name in product(
            arguments.regions, arguments.distributions):

            # Grab the region objects
            region1 = getattr(regions_file1, region_name)
            region2 = getattr(regions_file2, region_name)

            # Grab the distribution
            distribution = distributions[distribution_name]

            # Create the signal histogram
            histograms1 = []
            histograms2 = []
            count1 = 0
            count2 = 0
            for process_name in arguments.processes:
                # Extract parameters
                process1 = getattr(model_file1, process_name)
                process2 = getattr(model_file2, process_name)

                # Get the histograms
                histogram1 = distribution(process1, region1)
                histogram2 = distribution(process2, region2)

                # Append to the list
                histograms1.append(histogram1)
                histograms2.append(histogram2)

            # If we're in capture mode, the histograms are bogus, so ignore
            # them
            if parallel.capturing():
                continue

            histogram1 = combined_histogram(histograms1)
            histogram1.SetTitle(arguments.title_1)
            histogram2 = combined_histogram(histograms2)
            histogram2.SetTitle(arguments.title_2)

            # Add text output if requested
            if arguments.text_counts:
                # Compute the text output path
                text_output_path = join(arguments.output,
                                        region_name,
                                        '{0}.txt'.format(distribution_name))

                # Save text
                with open(text_output_path, 'w') as f:
                    # Print out histogram content
                    for h in [histogram1, histogram2]:
                        if h is None:
                            continue

                        f.write('--- {} ---\n'.format(h.GetTitle()))
                        f.write('Entries:  {:.1f}\n'.format(h.GetEntries()))
                        f.write('Integral: {:.1f}\n'.format(integral(h, False)))
                        f.write('Overflow: {:.1f}\n'.format(integral(h, True)))
                        for i, (b,v,e) in zip(range(h.GetNbinsX()+2),
                                                    get_bins_errors(h, True)):
                            f.write('{:4d} ({:5.1f}, {:6.1f}±{:.1f})\n'. \
                                    format(i, b, v, e))
                        f.write('\n')

            # Set all histogram titles to include their counts
            if not arguments.no_counts:
                for h in [histogram1, histogram2]:
                    if h is None:
                        continue

                    h.SetTitle('{0} ({1:.1f})'. \
                               format(h.GetTitle(), integral(h, False)))

            # Create a plot
            plot = Plot('',
                        distribution.x_label(),
                        distribution.y_label(),
                        ratio = True)

            if arguments.ratio_title is not None:
                ratio_title = arguments.ratio_title
            else:
                ratio_title = '#frac{{{}}}{{{}}}'.format(
                    histogram1.GetTitle(),
                    histogram2.GetTitle())
            ratio = ratio_histogram(histogram1, histogram2, ratio_title)
            
            # Draw histograms
            plot.draw((histogram1, default_black, 'ep'),
                      (histogram2, default_red, 'ep'))
            # Draw ratio
            plot.draw_ratio_histogram(ratio)
            # Draw legend
            plot.draw_legend()

            # Draw an ATLAS stamp
            label = region1.label()
            if region1.label() != region2.label():
                label += region2.label()
            if arguments.label:
                label += arguments.label
            plot.draw_atlas_label(luminosity = luminosity,
                                  sqrt_s = sqrt_s,
                                  custom_label = label,
                                  atlas_label = arguments.atlas_label)

            # Compute the plot output path
            plot_output_path = join(arguments.output,
                                    region_name,
                                    distribution_name)

            # Save plot
            plot.save(plot_output_path, arguments.extensions)
