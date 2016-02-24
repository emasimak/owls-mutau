#!/usr/bin/env python
#encoding: utf-8

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
from owls_hep.utility import efficiency, add_histograms, integral
from owls_hep.plotting import Plot, style_line
from owls_hep.uncertainty import to_shape, sum_quadrature

# owls-taunu imports
from owls_taunu.variations import Filtered, OneProng, ThreeProng
from owls_taunu.styling import default_black, default_red
from owls_taunu.plotting import plot, plot2d
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
parser.add_argument('-t',
                    '--text-output',
                    action = 'store_true',
                    help = 'enable text output of counts for systematic '
                    'variations')
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
    #'tau25_3p': {
        #'label': ['HLT_tau25_medium1_tracktwo'],
        #'region': three_prong,
        #'title': ' (3-prong)',
        #'distribution': distributions_file.tau_pt_trig_b1,
        #'filter': triggered_tau25,
    #},

    #'tau25_noiso_1p': {
        #'label': ['HLT_tau25_medium1_tracktwo_L1TAU12'],
        #'region': one_prong,
        #'title': ' (1-prong)',
        #'distribution': distributions_file.tau_pt_trig_b1,
        #'filter': triggered_tau25_noiso,
    #},
    #'tau25_noiso_3p': {
        #'label': ['HLT_tau25_medium1_tracktwo_L1TAU12'],
        #'region': three_prong,
        #'title': ' (3-prong)',
        #'distribution': distributions_file.tau_pt_trig_b1,
        #'filter': triggered_tau25_noiso,
    #},

    # TODO: Add tau35, tau80, tau125
})

# NOTE: See model file for comments about pruning
systematics = [
    #TestSystFlat,
    #TestSystShape,
    RqcdStat,
    RqcdSyst,
    MuonEffStat,
    MuonEffSys,
    MuonEffTrigStat,
    MuonEffTrigSys,
    #MuonIsoStat,
    #MuonIsoSys,
    #MuonIdSys,
    #MuonMsSys,
    #MuonScaleSys,
    BJetEigenB0,
    BJetEigenB1,
    #BJetEigenB2,
    #BJetEigenB3,
    #BJetEigenB4,
    #BJetEigenC0,
    #BJetEigenC1,
    #BJetEigenC2,
    #BJetEigenC3,
    #BJetEigenLight0,
    #BJetEigenLight1,
    #BJetEigenLight2,
    #BJetEigenLight3,
    #BJetEigenLight4,
    #BJetEigenLight5,
    #BJetEigenLight6,
    #BJetEigenLight7,
    #BJetEigenLight8,
    #BJetEigenLight9,
    #BJetEigenLight10,
    #BJetEigenLight11,
    #BJetEigenLight12,
    #BJetEigenLight13,
    #BJetExtrapolation,
]

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

# Open root file for output
if arguments.text_output:
    text_file =  open(join(base_path, 'tau_efficiencies_counts.txt'), 'w')

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
        #print('{} total/passed: {:.1f}/{:.1f}'. \
              #format(process.label(),
                     #integral(backgrounds_total[-1]),
                     #integral(backgrounds_passed[-1])))

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

    systs_total_up = {}
    systs_total_down = {}
    systs_passed_up = {}
    systs_passed_down = {}
    for s in systematics:
        name = s.name
        systs_total_up[name] = []
        systs_total_down[name] = []
        systs_passed_up[name] = []
        systs_passed_down[name] = []
        for background in itervalues(backgrounds):
            # Extract parameters
            process = background['process']
            estimation = background['estimation']
            uncertainties = background['uncertainties']

            nominal_total = estimation(distribution)(process, region)
            nominal_passed = estimation(distribution)(
                process, region.varied(efficiency_filter))

            if s in uncertainties:
                # Get the up/down of the total
                _, _, up, down = to_shape(
                    s(estimation(distribution))(process, region),
                    nominal_total)
                if up is not None and down is not None:
                    systs_total_up[name].append(up)
                    systs_total_down[name].append(down)
                else:
                    raise RuntimeError('something went wrong when applying '
                                       'systematic variation ' + s.name)

                # Get the up/down of the passed
                _, _, up, down = to_shape(
                    s(estimation(distribution))(
                        process, region.varied(efficiency_filter)),
                    nominal_passed)
                if up is not None and down is not None:
                    systs_passed_up[name].append(up)
                    systs_passed_down[name].append(down)
                else:
                    raise RuntimeError('something went wrong when applying '
                                       'systematic variation ' + s.name)
            else:
                #print('No systematic {} for {}. Using nominal.'. \
                      #format(name, process.label()))
                systs_total_up[name].append(nominal_total)
                systs_total_down[name].append(nominal_total)
                systs_passed_up[name].append(nominal_passed)
                systs_passed_down[name].append(nominal_passed)

            #print('{} up {} total/passed: {:.1f}/{:.1f}'. \
                  #format('NOMINAL',
                         #process.label(),
                         #integral(nominal_total),
                         #integral(nominal_passed)))
            #print('{} up {} total/passed: {:.1f}/{:.1f}'. \
                  #format(name,
                         #process.label(),
                         #integral(systs_total_up[name][-1]),
                         #integral(systs_passed_up[name][-1])))
            #print('{} down {} total/passed: {:.1f}/{:.1f}'. \
                  #format(name,
                         #process.label(),
                         #integral(systs_total_down[name][-1]),
                         #integral(systs_passed_down[name][-1])))


    # If capturing at pass 1, the result is bogus, continue
    if parallel.capturing():
        return None,None,None,None

    ##############################################################
    # COMPUTE SIGNAL EFFICIENCY
    ##############################################################
    signal_total = add_histograms(signals_total, 'Signal')
    signal_passed = add_histograms(signals_passed, 'Signal')

    write_counts_signal(signal_total, signal_passed)

    signal_efficiency = efficiency(signal_total, signal_passed)
    signal_efficiency.SetTitle('MC')


    ##############################################################
    # COMPUTE NOMINAL DATA EFFICIENCY
    ##############################################################
    background_total = add_histograms(backgrounds_total, 'Bkg')
    background_passed = add_histograms(backgrounds_passed, 'Bkg')
    data_subtracted_total = data_total - background_total
    data_subtracted_passed = data_passed - background_passed
    data_efficiency = efficiency(data_subtracted_total, data_subtracted_passed)
    data_efficiency.SetTitle('Data')

    ##############################################################
    # COMPUTE EFFICIENCIES FOR SYSTEMATIC VARIATIONS
    ##############################################################
    data_efficiency_up = []
    data_efficiency_down = []
    total_offset_up = []
    total_offset_down = []
    passed_offset_up = []
    passed_offset_down = []
    for s in systematics:
        name = s.name
        # NOTE: The up variation of the background removes a larger amount of
        # the data, leaving a smaller remainder. Thus the up variation of the
        # remainder is the data minus the down variation of the background,
        # and vice versa.
        syst_total_up = add_histograms(systs_total_up[name], 'Bkg')
        syst_passed_up = add_histograms(systs_passed_up[name], 'Bkg')
        data_subtracted_total_down = data_total - syst_total_up
        data_subtracted_passed_down = data_passed - syst_passed_up

        syst_total_down = add_histograms(systs_total_down[name], 'Bkg')
        syst_passed_down = add_histograms(systs_passed_down[name], 'Bkg')
        data_subtracted_total_up = data_total - syst_total_down
        data_subtracted_passed_up = data_passed - syst_passed_down

        total_offset_up.append(integral(data_subtracted_total_up) -
                               integral(data_subtracted_total))
        total_offset_down.append(integral(data_subtracted_total) -
                                 integral(data_subtracted_total_down))
        passed_offset_up.append(integral(data_subtracted_passed_up) -
                               integral(data_subtracted_passed))
        passed_offset_down.append(integral(data_subtracted_passed) -
                                 integral(data_subtracted_passed_down))

        write_counts_background(name, 'total',
                                data_subtracted_total,
                                data_subtracted_total_up,
                                data_subtracted_total_down)
        write_counts_background(name, 'passed',
                                data_subtracted_passed,
                                data_subtracted_passed_up,
                                data_subtracted_passed_down)

        # Compute the efficiencies
        data_efficiency_up.append(efficiency(data_subtracted_total_up,
                                             data_subtracted_passed_up))
        data_efficiency_down.append(efficiency(data_subtracted_total_down,
                                               data_subtracted_passed_down))

        data_efficiency_up[-1].SetTitle(name + '_UP')
        data_efficiency_down[-1].SetTitle(name + '_DOWN')

    write_total_syst('total',
                     integral(data_subtracted_total),
                     sum_quadrature(total_offset_up),
                     sum_quadrature(total_offset_down))
    write_total_syst('total',
                     integral(data_subtracted_passed),
                     sum_quadrature(passed_offset_up),
                     sum_quadrature(passed_offset_down))

    return data_efficiency, signal_efficiency, \
            data_efficiency_up, data_efficiency_down


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

    if not sf_x:
        raise RuntimeError('failed to create scale factors; '
                           'scale factor array is empty')

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
                 variation_efficiencies,
                 scale_factors,
                 file_name_components):
    root_file.cd()

    clone = data_efficiency.Clone(uuid4().hex)
    clone.SetName(
        '_'.join(['eff'] + file_name_components + ['data']))
    clone.Write()

    clone = signal_efficiency.Clone(uuid4().hex)
    clone.SetName(
        '_'.join(['eff'] + file_name_components + ['mc']))
    clone.Write()

    for eff in variation_efficiencies:
        clone = eff.Clone(uuid4().hex)
        clone.SetName(
            '_'.join(['eff'] + file_name_components + [clone.GetTitle()]))
        clone.Write()

    if scale_factors is not None:
        clone = scale_factors.Clone(uuid4().hex)
        clone.SetName('_'.join(['sf'] + file_name_components))
        clone.Write()

def write_counts_signal(total, passed):
    text_file.write('Signal total/passed: {:.1f}/{:.1f}\n'. \
                    format(integral(total), integral(passed)))

def write_total_syst(what, nominal_count, up_offset, down_offset):
    text_file.write('{:30s} {:10s}: {:6.1f} ({:5.2f}%) | {:6.1f} | '
                    '{:6.1f} ({:5.2f}%)\n'. \
                    format('ALL',
                           what,
                           nominal_count - down_offset,
                           -down_offset / nominal_count * 100.0,
                           nominal_count,
                           nominal_count + up_offset,
                           up_offset / nominal_count * 100.0))

def write_counts_background(syst, what, nominal, up, down):
    nominal, up, down = integral(nominal), integral(up), integral(down)
    def percentage(var):
        return (var/nominal - 1.0) * 100.0
    pc_up, pc_down = percentage(up), percentage(down)
    text_file.write('{:30s} {:10s}: {:6.1f} ({:5.2f}%) | {:6.1f} | '
                    '{:6.1f} ({:5.2f}%)\n'. \
                    format(syst, what, down, pc_down, nominal, up, pc_up))


# Run in a cached environment
with caching_into(cache):

    # Run in a parallelized environment
    while parallel.run():
        if parallel.computed():
            print('Computing efficiencies...')

        for eff_name, eff in iteritems(efficiencies):
            distribution = eff['distribution']
            efficiency_filter = eff['filter']
            region = eff['region']

            if arguments.text_output and not parallel.capturing():
                text_file.write('Efficiencies for {}\n'.format(eff_name))

            label = [region.label() + eff['title'], model['label']] + \
                    eff['label']

    ##############################################################
    # CREATE AND PLOT NOMINAL EFFICIENCIES AND SCALE FACTORS
    ##############################################################

            # Compute and plot the efficiencies
            data_efficiency, signal_efficiency, \
                    data_efficiency_up, data_efficiency_down = \
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
                             data_efficiency_up + data_efficiency_down,
                             scale_factor,
                             [eff_name])

if arguments.text_output:
    text_file.close()

if arguments.root_output:
    root_file.ls()
    root_file.Close()
