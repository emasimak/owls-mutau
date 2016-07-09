#!/usr/bin/env python
import argparse
from os import makedirs
from os.path import join, exists
from itertools import product

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.plotting import Plot, histogram_stack
from owls_hep.utility import integral

Plot.PLOT_Y_AXIS_TITLE_OFFSET = 1.5

usage_desc = '''\
Draw true taus, lepton fakes, b-jet fakes, and light jet fakes.
'''

parser = argparse.ArgumentParser(description = usage_desc)
parser.add_argument('-o',
                    '--output',
                    default = 'plots',
                    help = 'the plot output directory',
                    metavar = '<output>')
parser.add_argument('-R',
                    '--regions-file',
                    required = True,
                    help = 'the path to the region definition module',
                    metavar = '<regions-file>')
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
parser.add_argument('-l',
                    '--label',
                    nargs = '*',
                    help = 'items to add to the custom label',
                    metavar = '<items>')
parser.add_argument('-t',
                    '--text-counts',
                    action = 'store_true',
                    help = 'enable text output of counts')
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


model_file = load_module(arguments.model_file, definitions)
regions_file = load_module(arguments.regions_file, definitions)
distributions_file = load_module(arguments.distributions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)

# Extract regions
regions = dict((
    (r, getattr(regions_file, r))
    for r
    in arguments.regions
))

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


base_path = arguments.output
if not exists(base_path):
    makedirs(base_path)

def print_counts(file_name, names, counts, total):
    with open(file_name, 'w') as f:
        for n,c in zip(names,counts):
            f.write('{:30s}: {:.0f} ({:.1f})\n'.format(n, c, c/total*100.0))

# Run in a cached environment
with caching_into(cache):
    while parallel.run():
        for region_name, distribution_name in product(regions, distributions):
            region = regions[region_name]
            distribution = distributions[distribution_name]

            if not parallel.capturing():
                print('Processing region {}, distribution {}'. \
                      format(region_name, distribution_name))

            # Fetch the distributions
            if not parallel.capturing():
                print('  Fetching true taus...')
            true_taus = distribution(model_file.ttbar_true, region)
            if not parallel.capturing():
                print('  Fetching lep fakes...')
            lep_fakes = distribution(model_file.ttbar_lfake, region)
            if not parallel.capturing():
                print('  Fetching light jet fakes...')
            light_jet_fakes = distribution(model_file.ttbar_lightjetfake, region)
            if not parallel.capturing():
                print('  Fetching b-jet fakes...')
            b_jet_fakes = distribution(model_file.ttbar_bjetfake, region)

            # If we're in capture mode, the histograms are bogus, so ignore
            # them
            if parallel.capturing():
                continue

            # Setup counts and labels for counts file
            hists = [true_taus, lep_fakes, light_jet_fakes, b_jet_fakes]
            names = ['True tau', 'Lepton fakes', 'b-jet fakes', 'light jet fakes']
            counts = [integral(h) for h in hists]
            total = sum(counts)
            if total == 0:
                total = 1.0

            # Write counts
            if arguments.text_counts:
                text_output_path = join(base_path,
                                        '{}_{}.txt'.format(region_name,
                                                           distribution_name))
                print_counts(text_output_path, names, counts, total)

            # Add counts to histogram titles
            for h,c in zip(hists, counts):
                h.SetTitle('{} {:.0f} ({:.1f}%)'. \
                           format(h.GetTitle(), c, c/total*100.0))

            # Create the histogram stack
            stack = histogram_stack(light_jet_fakes, b_jet_fakes, lep_fakes, true_taus)

            # Draw the plot
            plot = Plot('',
                        distribution.x_label(),
                        '[a.u.]',
                        y_max = 20000.0,
                        ratio = False)

            plot.draw((stack, None, 'hist'))
            plot.draw_legend()
            label = region.label()
            if arguments.label is not None:
                label.append(arguments.label)
            plot.draw_atlas_label(custom_label = label)
            plot.save(join(base_path,
                           '{}_{}'.format(region_name,
                                          distribution_name)),
                      arguments.extensions)
