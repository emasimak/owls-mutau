#!/usr/bin/env python
# encoding: utf-8

# System imports
import argparse
from math import sqrt

# Six imports
from six import itervalues, iteritems, iterkeys

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.counting import Count
from owls_hep.utility import integral
from owls_hep.histogramming import Histogram

# owls-taunu imports
from owls_taunu.mutau.variations import OS, SS

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Compute r_QCD'
)
parser.add_argument('-M',
                    '--model-file',
                    required = True,
                    help = 'the path to the model definition module',
                    metavar = '<model-file>')
#parser.add_argument('-m',
                    #'--model',
                    #required = True,
                    #help = 'the model to plot',
                    #metavar = '<model>')
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
parser.add_argument('-o',
                    '--output',
                    help = 'the path to the file where to store the output '
                    'of the computation',
                    metavar = '<environment-file>')
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
data = model_file.data

# Extract regions
regions = dict((
    (r, getattr(regions_file, r))
    for r
    in arguments.regions
))

met_et = Histogram(
        'met_et / 1000.0',
        (15, 0, 300),
        '',
        'E_{T}^{miss} (GeV)',
        'Events / 20 GeV'
        )

# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
#cache = None

r_qcd_dict = {}

# Run in a cached environment
with caching_into(cache):
    # Loop over regions
    for region_name in regions:
        region = regions[region_name]
        met_et_os = met_et(data, region.varied(OS()))
        met_et_ss = met_et(data, region.varied(SS()))
        #print('MET ET OS = {0:.2f}, SS = {1:.2f}'.format(
            #integral(met_et_os, include_overflow=True),
            #integral(met_et_ss, include_overflow=True)))

        ss_counts = Count()(data, region.varied(SS()))
        ss_uncertainty = sqrt(ss_counts)
        os_counts = Count()(data, region.varied(OS()))
        os_uncertainty = sqrt(os_counts)
        print('{0}: Counts OS = {1:.0f}±{2:.1f}, SS = {3:.0f}±{4:.1f}'. \
              format(region.label(),
                     os_counts,
                     os_uncertainty,
                     ss_counts,
                     ss_uncertainty))

        r_qcd = os_counts / ss_counts
        r_qcd_uncertainty = sqrt((os_uncertainty / os_counts)**2 +
                                 (ss_uncertainty / ss_counts)**2) * r_qcd
        # Round to 3 decimals
        r_qcd, r_qcd_uncertainty = round(r_qcd, 3), round(r_qcd_uncertainty, 3)
        r_qcd_dict[region_name] = (r_qcd, r_qcd_uncertainty)
        print('{0}: r_QCD = {1:.2f} ± {2:.2f}'. \
              format(region.label(), r_qcd, r_qcd_uncertainty))

if arguments.output is not None:
    with open(arguments.output, 'w') as f:
        f.write(str(r_qcd_dict))
        f.write('\n')
