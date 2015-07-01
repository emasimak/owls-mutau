#!/usr/bin/env python


# System imports
import argparse
from os import makedirs
from os.path import join, exists, isdir
from itertools import product, chain
from functools import partial
from math import sqrt
from random import shuffle

# Six imports
from six import itervalues, iteritems, iterkeys

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.plotting import Plot
from owls_hep.estimation import Plain
from owls_hep.histogramming import integral

from owls_taunu.taujets.variations import Triggered, TruthMatched
from owls_taunu.taujets.styling import create_style, \
        style as style_drawable

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Generate plots for trigger matching tool'
)
parser.add_argument('-o',
                    '--output',
                    default = 'plots',
                    help = 'the plot output directory',
                    metavar = '<output>')
parser.add_argument('-M',
                    '--model-file',
                    required = True,
                    help = 'the path to the model definition module',
                    metavar = '<model-file>')
parser.add_argument('-R',
                    '--regions-file',
                    required = True,
                    help = 'the path to the region definition module',
                    metavar = '<regions-file>')
parser.add_argument('-D',
                    '--distributions-file',
                    required = True,
                    help = 'the path to the histograms definition module',
                    metavar = '<distributions-file>')
parser.add_argument('-E',
                    '--environment-file',
                    required = True,
                    help = 'the path to the environment definition module',
                    metavar = '<environment-file>')
parser.add_argument('-n',
                    '--no-counts',
                    action = 'store_true',
                    help = 'disable event counts in legends')
parser.add_argument('definitions',
                    nargs = '*',
                    help = 'definitions to use within modules in the form x=y',
                    metavar = '<definition>')
arguments = parser.parse_args()


# Parse definitions
definitions = dict((d.split('=') for d in arguments.definitions))


# Load files
model_file = load_module(arguments.model_file, definitions)
regions_file = load_module(arguments.regions_file, definitions)
distributions_file = load_module(arguments.distributions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)


# Get processes
processes = model_file.processes
sqrt_s = model_file.sqrt_s
luminosity = model_file.luminosity

# Get the region specification and set the region name
regions = {
    'baseline': regions_file.baseline,
    'baseline_loose': regions_file.baseline_loose,
}

distributions = {
    'tau_pt': distributions_file.tau_pt,
    'tau_eta': distributions_file.tau_eta,
    'tau_phi': distributions_file.tau_phi,
    'tau_hlt_pt': distributions_file.tau_hlt_pt,
    #'tau_hlt_eta': distributions_file.tau_hlt_eta,
    #'tau_hlt_phi': distributions_file.tau_hlt_phi,
}

triggers = [
    'HLT_tau35_medium1_tracktwo',
    'HLT_tau125_medium1_tracktwo',
]


# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
backend = getattr(environment_file, 'parallelization_backend', None)


# Create the parallelization environment
parallel = ParallelizedEnvironment(backend)

def process_combination(region_name, process_name, distribution_name,
                        trigger, path):

    distribution = distributions[distribution_name]
    process = processes[process_name]
    region = regions[region_name]


    trig = region.varied(Triggered(trigger))
    trig_matched = region.varied(Triggered(trigger, matched=True))
    trig_antimatched = region.varied(Triggered(trigger, matched=False))


    # Compute the histograms
    trig_hist = Plain(distribution)(process, trig)
    trig_hist_matched = Plain(distribution)(process, trig_matched)
    trig_hist_antimatched = Plain(distribution)(process, trig_antimatched)

    trig_hist.SetTitle('{0} ({1})'.format(trig_hist.GetTitle(), trigger))
    trig_hist_matched.SetTitle('{0} ({1})'. \
            format(trig_hist_matched.GetTitle(),
                   'Matched {0}'.format(trigger)))
    trig_hist_antimatched.SetTitle('{0} ({1})'. \
            format(trig_hist_antimatched.GetTitle(),
                   'Anti-matched {0}'.format(trigger)))

    print('Processing {0}/{1} {2}:{3}'. \
            format(region_name,
                   process_name,
                   distribution_name,
                   trigger))

    # If we're in capture mode, the histograms are bogus, so
    # ignore them
    if parallel.capturing():
        return
    else:
        plot_histogram((trig_hist, trig_hist_matched, trig_hist_antimatched),
                       path,
                       region_name,
                       process_name,
                       distribution_name,
                       trigger)


def plot_histogram(hists, path, region_name, process_name,
                   distribution_name, trigger):

    distribution = distributions[distribution_name]
    region = regions[region_name]

    # Include passed/total counts in graph objects
    if not arguments.no_counts:
        for h in hists:
            h.SetTitle('{0} ({1:.1f})'.format(
                h.GetTitle(),
                integral(h)
            ))

    # Style the histograms (style is of size 8, make sure size of hists is
    # equal or smaller than that)
    # TODO: Using divergent style because nothing else is available at the
    # time of writing. To be changed when sequential styles are included.
    styles = create_style('divergent', 5)
    for h,s in zip(hists, (styles[1], styles[-2], styles[-4])):
        style_drawable(h, *s)

    # Create the plot
    plot = Plot('',
                distribution.x_label(),
                distribution.y_label())
    plot.draw(*zip(hists, ['ep']*3))
    # Draw a legend
    plot.draw_legend(hists)
    # Draw an ATLAS stamp
    plot.draw_atlas_label(custom_label = region.label(),
                          atlas_label = None)

    # Compute the plot output path
    parts = [distribution_name, process_name, region_name, trigger]
    output_name = '{0}.pdf'.format('_'.join(parts))

    # Save plot
    plot.save(join(path, output_name))

# Run in a cached environment
with caching_into(cache):

    # Run in a parallelized environment
    while parallel.run():

        # Loop over processes and regions (they result in individual output)
        for process_name, region_name \
                in product(iterkeys(processes), iterkeys(regions)):

            # Create the directories for the different processes
            if not exists(arguments.output):
                makedirs(arguments.output)

            # Loop over distributions
            for distribution_name in iterkeys(distributions):

                # Loop over triggers
                for trigger in triggers:

                    process_combination(region_name,
                                        process_name,
                                        distribution_name,
                                        trigger,
                                        arguments.output)

