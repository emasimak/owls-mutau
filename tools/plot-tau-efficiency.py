#!/usr/bin/env python

# System imports
import argparse
from os import makedirs
from os.path import join, exists
from collections import OrderedDict
from math import sqrt
from array import array
from uuid import uuid4

# Six imports
from six import itervalues, iteritems, iterkeys

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.utility import efficiency, add_histograms
from owls_hep.plotting import Plot, style_line

# owls-taunu imports
from owls_taunu.variations import Filtered, OneProng, ThreeProng
from owls_taunu.styling import default_black, default_red
from owls_taunu.plotting import plot, plot2d

# ROOT imports
from ROOT import TGraphAsymmErrors, TFile, SetOwnership

Plot.PLOT_LEGEND_LEFT = 0.55
Plot.PLOT_LEGEND_RIGHT = 1.0
Plot.PLOT_LEGEND_TOP = 0.88
Plot.PLOT_HEADER_HEIGHT = 300

ATLAS_LABEL = 'Internal'

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Generate plots and a combined plotbook'
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
                    help = 'the model to compute efficencies for',
                    metavar = '<model>')
parser.add_argument('-R',
                    '--regions-file',
                    required = True,
                    help = 'the path to the region definition module',
                    metavar = '<regions-file>')
parser.add_argument('-r',
                    '--region',
                    required = True,
                    help = 'the region to compute efficiencies for',
                    metavar = '<region>')
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
parser.add_argument('--root-output',
                    action = 'store_true',
                    help = 'write plotted histograms to a ROOT file',
                   )
parser.add_argument('--scale-factors',
                    action = 'store_true',
                    help = 'plot scale factors',
                   )
parser.add_argument('--variations',
                    action = 'store_true',
                    help = 'do variations',
                   )
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
distributions_file = load_module(arguments.distributions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)


# Extract model
model = getattr(model_file, arguments.model)
region = getattr(regions_file, arguments.region)
luminosity = model['luminosity']
sqrt_s = model['sqrt_s']
data = model['data']
signals = model['signals']
backgrounds = model['backgrounds']


one_prong = region.varied(OneProng())
three_prong = region.varied(ThreeProng())


triggered_tau25 = Filtered('HLT_tau25_medium1_tracktwo && '
                           'tau_0_trig_HLT_tau25_medium1_tracktwo')
triggered_tau25_noiso = Filtered('HLT_tau25_medium1_tracktwo_L1TAU12 && '
                                  'tau_0_trig_HLT_tau25_medium1_tracktwo_L1TAU12')

triggered_tau35 = Filtered('HLT_tau35_medium1_tracktwo && '
                           'tau_0_trig_HLT_tau35_medium1_tracktwo')
triggered_tau80 = Filtered('HLT_tau80_medium1_tracktwo && '
                           'tau_0_trig_HLT_tau80_medium1_tracktwo')
triggered_tau125 = Filtered('HLT_tau125_medium1_tracktwo && '
                           'tau_0_trig_HLT_tau125_medium1_tracktwo')

efficiencies = OrderedDict({
    'tau25_1p': {
        'label': ['HLT_tau25_medium1_tracktwo'],
        'region': one_prong,
        'title': ' (1-prong)',
        'distribution': distributions_file.tau_pt_trig_b1,
        'filter': triggered_tau25,
    },
    'tau25_3p': {
        'label': ['HLT_tau25_medium1_tracktwo'],
        'region': three_prong,
        'title': ' (3-prong)',
        'distribution': distributions_file.tau_pt_trig_b1,
        'filter': triggered_tau25,
    },

    'tau25_noiso_1p': {
        'label': ['HLT_tau25_medium1_tracktwo_L1TAU12'],
        'region': one_prong,
        'title': ' (1-prong)',
        'distribution': distributions_file.tau_pt_trig_b1,
        'filter': triggered_tau25_noiso,
    },
    'tau25_noiso_3p': {
        'label': ['HLT_tau25_medium1_tracktwo_L1TAU12'],
        'region': three_prong,
        'title': ' (3-prong)',
        'distribution': distributions_file.tau_pt_trig_b1,
        'filter': triggered_tau25_noiso,
    },

    # TODO: Add tau35, tau80, tau125
})

# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
backend = getattr(environment_file, 'parallelization_backend', None)

# Create the parallelization environment
parallel = ParallelizedEnvironment(backend)

# Create the directories for the different processes
base_path = arguments.output
if not exists(base_path):
    makedirs(base_path)

# Open root file for output
if arguments.root_output:
    root_file =  TFile.Open(join(base_path, 'tau_efficiencies.root'),
                            'RECREATE')

print('Script options')
print('  Output directory: {}'.format(base_path))
print('  Data prefix: {}'.format(definitions.get('data_prefix', 'UNDEFINED')))

def do_efficiencies(distribution, region, efficiency_filter):
    ##############################################################
    # COMPUTE (DATA-BACKGROUND) AND SIGNAL HISTOGRAMS
    ##############################################################
    data_total = distribution(data['process'], region)
    data_passed = distribution(data['process'],
                               region.varied(efficiency_filter))

    backgrounds_total = []
    backgrounds_passed = []
    for background in itervalues(backgrounds):
        # Extract parameters
        process = background['process']
        estimation = background['estimation']

        # Compute the total and passed histograms
        backgrounds_total.append(
            estimation(distribution)(process, region)
        )
        backgrounds_passed.append(
            estimation(distribution)(
                process, region.varied(efficiency_filter)
            )
        )

    # Loop over signal samples and compute their histograms
    signals_total = []
    signals_passed = []
    for signal in itervalues(signals):
        # Extract parameters
        process = signal['process']
        estimation = signal['estimation']

        # Compute the total and passed histograms
        signals_total.append(
            estimation(distribution)(process, region)
        )
        signals_passed.append(
            estimation(distribution)(
                process, region.varied(efficiency_filter)
            )
        )

    # If capturing at pass 1, the result is bogus, continue
    if parallel.capturing():
        return None,None

    # Create combined background histogram and subtract from
    # data
    if len(backgrounds_total) > 0:
        background_total = add_histograms(backgrounds_total, 'MC')
        background_passed = add_histograms(backgrounds_passed, 'MC')
        data_total = data_total - background_total
        data_passed = data_passed - background_passed


    # Create combined signal histograms
    signal_total = add_histograms(signals_total, 'Signal')
    signal_passed = add_histograms(signals_passed, 'Signal')

    ##############################################################
    # COMPUTE EFFICIENCIES
    ##############################################################

    # Compute the efficiencies
    data_efficiency = efficiency(data_total, data_passed)
    signal_efficiency = efficiency(signal_total, signal_passed)

    data_efficiency.SetTitle('Data')
    signal_efficiency.SetTitle('MC')

    return data_efficiency, signal_efficiency

def plot_efficiencies(data_efficiency,
                      signal_efficiency,
                      distribution,
                      path,
                      file_name_components,
                      label):
    efficiencies = [
        (signal_efficiency, default_red, 'e2'),
        (data_efficiency, default_black, 'ep')
    ]

    # Compute the plot output path
    save_path = join(path,
            '_'.join(file_name_components))

    plot(efficiencies,
         save_path,
         x_label = distribution.x_label(),
         y_label = distribution.y_label(),
         custom_label = label,
         atlas_label = ATLAS_LABEL,
         extensions = arguments.extensions)

def do_scale_factor(data_efficiency, signal_efficiency):
    ##############################################################
    # COMPUTE SCALE FACTORS
    ##############################################################
    points = data_efficiency.GetN()
    x_data = data_efficiency.GetX()
    error_x_data = data_efficiency.GetEXlow()
    y_data = data_efficiency.GetY()
    error_low_data = data_efficiency.GetEYlow()
    error_high_data = data_efficiency.GetEYhigh()
    y_background = signal_efficiency.GetY()
    error_low_background = signal_efficiency.GetEYlow()
    error_high_background = signal_efficiency.GetEYhigh()
    sf_x, sf_y, error_x, error_low, error_high = [], [], [], [], []
    for i in xrange(points):
        try:
            sf = y_data[i] / y_background[i]
            sf_x.append(x_data[i])
            sf_y.append(sf)
            error_x.append(error_x_data[i])
            error_low.append(sf * \
                    sqrt((error_low_data[i] / y_data[i])**2 + \
                         (error_high_background[i] / y_background[i])**2))
            error_high.append(sf * \
                    sqrt((error_high_data[i] / y_data[i])**2 + \
                         (error_low_background[i] / y_background[i])**2))
        except ZeroDivisionError:
            pass

    # Create the scale factor histogram (Data/MC) and fill it
    scale_factor = TGraphAsymmErrors(len(sf_x),
                                     array('d', sf_x),
                                     array('d', sf_y),
                                     array('d', error_x),
                                     array('d', error_x),
                                     array('d', error_low),
                                     array('d', error_high)
                                    )
    try:
        scale_factor.SetTitle('Data / {}'.format(
                              definitions['background_model_label']))
    except:
        scale_factor.SetTitle('Data / MC')
    return scale_factor

def plot_scale_factor(scale_factor,
                      distribution,
                      path,
                      file_name_components,
                      label):
    # Compute the plot output path
    save_path = join(path,
            '_'.join(file_name_components + ['sf']))

    plot([(scale_factor, default_black, 'ep')],
         save_path,
         x_label = distribution.x_label(),
         y_label = distribution.y_label(),
         custom_label = label,
         atlas_label = ATLAS_LABEL,
         extensions = arguments.extensions)

def save_to_root(data_efficiency,
                 signal_efficiency,
                 scale_factors,
                 file_name_components):
    ##############################################################
    # SAVE EFFICIENCIES AND SCALE FACTORS TO A ROOT FILE
    ##############################################################
    root_file.cd()

    clone = data_efficiency.Clone(uuid4().hex)
    clone.SetName(
        '_'.join(['eff'] + file_name_components + ['data']))
    clone.Write()

    clone = signal_efficiency.Clone(uuid4().hex)
    clone.SetName(
        '_'.join(['eff'] + file_name_components + ['mc']))
    clone.Write()

    if scale_factors is not None:
        clone = scale_factors.Clone(uuid4().hex)
        clone.SetName('_'.join(['sf'] + file_name_components))
        clone.Write()

# Run in a cached environment
with caching_into(cache):

    # Run in a parallelized environment
    while parallel.run():
        if parallel.computed():
            print('Creating plots...')

        for eff_name, eff in iteritems(efficiencies):
            distribution = eff['distribution']
            efficiency_filter = eff['filter']
            region = eff['region']

            label = [region.label() + eff['title'], model['label']] + \
                    eff['label']

    ##############################################################
    # CREATE AND PLOT NOMINAL EFFICIENCIES AND SCALE FACTORS
    ##############################################################

            # Compute and plot the efficiencies
            data_efficiency, signal_efficiency = \
                do_efficiencies(distribution,
                                region,
                                efficiency_filter)

            # If capturing at pass 1, the efficiencies are bogus, continue
            if parallel.capturing():
                continue

            plot_efficiencies(data_efficiency,
                              signal_efficiency,
                              distribution,
                              base_path,
                              [eff_name],
                              label)

            # Compute and plot the scale factors
            scale_factor = \
                do_scale_factor(data_efficiency,
                                signal_efficiency)

            plot_scale_factor(scale_factor,
                              distribution,
                              base_path,
                              [eff_name],
                              label)


            # Save efficiencies and scale factors to a root file
            if arguments.root_output:
                save_to_root(data_efficiency,
                             signal_efficiency,
                             scale_factor,
                             [eff_name])

if arguments.root_output:
    root_file.ls()
    root_file.Close()
