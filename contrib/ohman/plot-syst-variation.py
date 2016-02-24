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
from owls_hep.plotting import Plot, style_histogram
from owls_hep.utility import integral

# owls-taunu imports
from owls_taunu.styling import default_black_line, default_red_line, \
        default_blue_line
from owls_taunu.mutau.uncertainties import TestSystFlat, TestSystShape, \
        MuonEffStat, MuonEffSys, \
        MuonEffTrigStat, MuonEffTrigSys, \
        MuonIsoStat, MuonIsoSys, \
        MuonIdSys, MuonMsSys, MuonScaleSys, \
        RqcdStat, RqcdSyst, \
        BJetEigenB0, BJetEigenB1, BJetEigenB2, BJetEigenB3, BJetEigenB4, \
        BJetEigenC0, BJetEigenC1, BJetEigenC2, BJetEigenC3, \
        BJetEigenLight0, BJetEigenLight1, BJetEigenLight2, BJetEigenLight3, \
        BJetEigenLight4, BJetEigenLight5, BJetEigenLight6, BJetEigenLight7, \
        BJetEigenLight8, BJetEigenLight9, BJetEigenLight10, BJetEigenLight11, \
        BJetEigenLight12, BJetEigenLight13, \
        BJetExtrapolation

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
parser.add_argument('--label', default=None,
                    help='Label for the plot')
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

systematics = [
    #TestSystFlat,
    TestSystShape,
    #RqcdStat, # no point in plotting overall systematics
    #RqcdSyst, # no point in plotting overall systematics
    MuonEffStat,
    MuonEffSys,
    MuonEffTrigStat,
    MuonEffTrigSys,
    MuonIsoStat,
    MuonIsoSys,
    MuonIdSys,
    MuonMsSys,
    MuonScaleSys,
    BJetEigenB0,
    BJetEigenB1,
    BJetEigenB2,
    BJetEigenB3,
    BJetEigenB4,
    BJetEigenC0,
    BJetEigenC1,
    BJetEigenC2,
    BJetEigenC3,
    BJetEigenLight0,
    BJetEigenLight1,
    BJetEigenLight2,
    BJetEigenLight3,
    BJetEigenLight4,
    BJetEigenLight5,
    BJetEigenLight6,
    BJetEigenLight7,
    BJetEigenLight8,
    BJetEigenLight9,
    BJetEigenLight10,
    BJetEigenLight11,
    BJetEigenLight12,
    BJetEigenLight13,
    BJetExtrapolation,
    #BJetExtrapolationCharm, # Doesn't work
]


base_path = arguments.output
if not exists(base_path):
    makedirs(base_path)

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
            nominal = distribution(model_file.ttbar, region)
            nominal += distribution(model_file.single_top, region)
            nominal.SetTitle('NOMINAL')

            for s in systematics:
                _,_,shape_up,shape_down = s(distribution)(model_file.ttbar, region)
                _,_,shape_up_addon,shape_down_addon = s(distribution)(model_file.single_top, region)

                # If we're in capture mode, the histograms are bogus, so ignore
                # them
                if parallel.capturing():
                    continue

                shape_up += shape_up_addon
                shape_down += shape_down_addon

                overall_up = integral(shape_up) / integral(nominal) - 1.0
                overall_down = integral(shape_down) / integral(nominal) - 1.0

                shape_up.SetTitle('{}_UP ({:.2f}%)'.format(s.name, overall_up*100.0))
                shape_down.SetTitle('{}_DOWN ({:.2f}%)'.format(s.name, overall_down*100.0))

                # Draw the plot
                plot = Plot('',
                            x_title = distribution.x_label(),
                            y_title = '[a.u.]')

                plot.draw(
                    (nominal, default_black_line, 'hist'),
                    (shape_up, default_red_line, 'hist'),
                    (shape_down, default_blue_line, 'hist')
                )

                plot.draw_legend()
                label = [region.label(), 't#bar{t} + Single top']
                if arguments.label is not None:
                    label.append(arguments.label)
                plot.draw_atlas_label(custom_label = label)
                plot.save(join(base_path,
                               '{}_{}_{}'.format(region_name,
                                                 distribution_name,
                                                 s.name)),
                          arguments.extensions)
