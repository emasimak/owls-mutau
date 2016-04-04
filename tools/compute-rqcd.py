#!/usr/bin/env python
# encoding: utf-8

# System imports
import argparse
from math import sqrt
from collections import OrderedDict
from os import makedirs
from os.path import join, exists

from six import iteritems

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.counting import Count
from owls_hep.utility import integral
from owls_hep.histogramming import Histogram
from owls_hep.plotting import Plot, ratio_histogram

# owls-taunu imports
from owls_taunu.mutau.variations import OS, SS
from owls_taunu.styling import default_black, default_red

Plot.PLOT_RATIO_Y_AXIS_TITLE_OFFSET = 0.50

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Compute r_QCD'
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
parser.add_argument('-m',
                    '--model',
                    required = True,
                    help = 'the model to plot',
                    metavar = '<model>')
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
parser.add_argument('-E',
                    '--environment-file',
                    required = True,
                    help = 'the path to the environment definition module',
                    metavar = '<environment-file>')
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


# Load files
model_file = load_module(arguments.model_file, definitions)
regions_file = load_module(arguments.regions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)


# Extract processes
model = getattr(model_file, arguments.model)
data = model['data']
backgrounds = model['backgrounds']

# Extract regions
regions = OrderedDict((
    (r, getattr(regions_file, r))
    for r
    in arguments.regions
))

ptcone_syst = Histogram(
    'lep_0_iso_ptvarcone30/lep_0_pt/1000.0',
    (30, 0.1, 0.4),
    '',
    'ptvarcone30/p_{T}',
    'Events'
)

etcone_syst = Histogram(
    'lep_0_iso_topoetcone20/lep_0_et/1000.0',
    (30, 0.1, 0.4),
    '',
    'topoetcone20/E_{T}',
    'Events'
)

# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
backend = getattr(environment_file, 'parallelization_backend', None)

# Create the parallelization environment
parallel = ParallelizedEnvironment(backend)

def sum_cumulative(histogram):
    for i in range(1, histogram.GetNbinsX()+1):
        cumulative_count = integral(histogram,
                                    bin_range = (i+1, histogram.GetNbinsX()+1))
        stat_error = sqrt(cumulative_count)
        histogram.SetBinContent(i, cumulative_count)
        histogram.SetBinError(i, stat_error)

def compute_syst(region, distribution, file_name):
    os = distribution(data['process'], region.varied(OS()))
    ss = distribution(data['process'], region.varied(SS()))
    #if not parallel.capturing():
        #print('Data OS/SS: {}/{}'.format(integral(os), integral(ss)))
    for name,background in iteritems(backgrounds):
        if name == 'ss_data':
            continue
        process = background['process']
        background_os = distribution(process, region.varied(OS()))
        background_ss = distribution(process, region.varied(SS()))
        #if not parallel.capturing():
            #print('{} OS/SS: {}/{}'.format(process.label(),
                                           #integral(background_os),
                                           #integral(background_ss)))
        os = os - background_os
        ss = ss - background_ss
        #if not parallel.capturing():
            #print('Sum OS/SS: {}/{}'.format(integral(os), integral(ss)))

    sum_cumulative(os)
    sum_cumulative(ss)
    ratio = ratio_histogram(os, ss)

    os.SetTitle('Opposite sign ({:.0f})'.format(os.GetBinContent(1)))
    ss.SetTitle('Same sign({:.0f})'.format(os.GetBinContent(1)))

    up = ratio.GetBinContent(ratio.GetMaximumBin())
    down = ratio.GetBinContent(ratio.GetMinimumBin())
    syst = abs(up-down)/2

    # Draw the plot
    plot = Plot('',
                x_title = distribution.x_label(),
                y_title = 'Events',
                ratio = True)

    plot.draw(
        (os, default_black, 'ep'),
        (ss, default_red, 'ep'),
    )
    mod = lambda v: round(v*20.0, 0) / 20.0
    plot.draw_ratios(
        [(ratio, default_black, 'ep')],
        y_range = (mod(down*0.95), mod(down*0.9) + 0.4),
        y_title = 'r_{QCD}'
    )

    plot.draw_legend()
    plot.draw_atlas_label(custom_label = [region.label()])
    plot.save(join(base_path, file_name), arguments.extensions)

    return syst

r_qcd_dict = OrderedDict({})

base_path = arguments.output
if not exists(base_path):
    makedirs(base_path)

# Run in a cached environment
with caching_into(cache):
    while parallel.run():
        # Loop over regions
        for region_name in regions:
            region = regions[region_name]

            # Get counts from data
            ss_counts = Count()(data['process'], region.varied(SS()))
            os_counts = Count()(data['process'], region.varied(OS()))

            # Subtract MC backgrounds
            for name,background in iteritems(backgrounds):
                if name == 'ss_data':
                    continue
                process = background['process']
                ss_counts -= Count()(process, region.varied(SS()))
                os_counts -= Count()(process, region.varied(OS()))

            r_qcd_raw_syst_ptcone = \
                    compute_syst(region,
                                 ptcone_syst,
                                 '{}_ptvarcone30'.format(region_name))
            r_qcd_raw_syst_etcone = \
                    compute_syst(region,
                                 etcone_syst,
                                 '{}_topoetcone20'.format(region_name))

            if parallel.capturing():
                continue

            ss_stat = sqrt(ss_counts)
            os_stat = sqrt(os_counts)

            print('{0}: Counts OS = {1:.0f}±{2:.1f}, SS = {3:.0f}±{4:.1f}'. \
                  format(region.label(),
                         os_counts,
                         os_stat,
                         ss_counts,
                         ss_stat))

            # Compute rQCD and errors
            r_qcd = os_counts / ss_counts
            r_qcd_stat = sqrt((os_stat / os_counts)**2 +
                                     (ss_stat / ss_counts)**2) * r_qcd
            r_qcd_syst_ptcone = r_qcd_raw_syst_ptcone / r_qcd
            r_qcd_syst_etcone = r_qcd_raw_syst_etcone / r_qcd
            r_qcd_syst = sqrt(r_qcd_syst_ptcone**2 + r_qcd_syst_etcone**2)

            # Round to 3 decimals
            r_qcd = round(r_qcd, 3)
            r_qcd_stat = round(r_qcd_stat, 3)
            r_qcd_syst = round(r_qcd_syst, 3)
            r_qcd_dict[region_name] = (r_qcd, r_qcd_stat, r_qcd_syst)

            # Print the result
            print('{}: r_QCD = {:.2f} ± {:.2f}(stat) ± '
                  '{:.2f}(pt) ± {:.2f}(et)'. \
                  format(region.label(), r_qcd, r_qcd_stat,
                         r_qcd_syst_ptcone, r_qcd_syst_etcone))
            print('{}: r_QCD = {:.2f} ± {:.2f}(stat) ± {:.2f}(syst)'. \
                  format(region.label(), r_qcd, r_qcd_stat, r_qcd_syst))

with open(join(base_path, 'rqcd.txt'), 'w') as f:
    for k,v in r_qcd_dict.iteritems():
        f.write('\'{}\': {},\n'.format(k, v))
