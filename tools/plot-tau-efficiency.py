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
from ROOT import TGraphAsymmErrors, TFile, SetOwnership, \
        kCyan, kBlue, kBlack, kRed

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
        'distribution': distributions_file.tau_pt_trig_b2,
        'filter': triggered_tau25,
    },
    'tau25_3p': {
        'label': ['HLT_tau25_medium1_tracktwo'],
        'region': three_prong,
        'title': ' (3-prong)',
        'distribution': distributions_file.tau_pt_trig_b2,
        'filter': triggered_tau25,
    },

    'tau25_ztt_1p': {
        'label': ['HLT_tau25_medium1_tracktwo'],
        'region': one_prong,
        'title': ' (1-prong)',
        'distribution': distributions_file.tau_pt_trig_b1,
        'filter': triggered_tau25,
    },
    'tau25_ztt_3p': {
        'label': ['HLT_tau25_medium1_tracktwo'],
        'region': three_prong,
        'title': ' (3-prong)',
        'distribution': distributions_file.tau_pt_trig_b1,
        'filter': triggered_tau25,
    },

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
    BJetEigenC0,
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
print('  Systematics treatment: {}'.format(model_file.systematics))

def normalize_efficiencies(nominal, up, down):
    if nominal.GetN() != up.GetN() or nominal.GetN() != down.GetN():
        raise RuntimeError('point count mismatch; nominal, up, and down '
                           'efficiencies have different number of points')
    values_x = nominal.GetX()
    values_y = nominal.GetY()
    values_y_up = up.GetY()
    values_y_down = down.GetY()
    for i, x, y, y_up, y_down in zip(range(nominal.GetN()),
                                     values_x, values_y,
                                     values_y_up, values_y_down):
        # Switch
        if y_up < y_down:
            #print('  Switching {:.2f} and {:.2f}'.format(y_up, y_down))
            y_up, y_down = y_down, y_up

        # If up variation is lower than nominal, reset
        if y_up < y:
            #print('  Resetting {} < {}'.format(y_up, y))
            y_up = y

        # If down variation is greater than nominal, reset
        if y_down > y:
            #print('  Resetting {} > {}'.format(y_down, y))
            y_down = y

        up.SetPoint(i, x, y_up)
        down.SetPoint(i, x, y_down)

def do_efficiencies(distribution, region, efficiency_filter):
    ##############################################################
    # COMPUTE (DATA-BACKGROUND) AND SIGNAL HISTOGRAMS
    ##############################################################
    process = data['process']
    estimation = data['estimation']
    data_total = estimation(distribution)(process, region)
    data_passed = estimation(distribution)(process,
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
                _, _, up, down = estimation(s(distribution))(process, region)
                if up is not None and down is not None:
                    systs_total_up[name].append(up)
                    systs_total_down[name].append(down)
                else:
                    raise RuntimeError('something went wrong when applying '
                                       'systematic variation ' + s.name)

                # Get the up/down of the passed
                _, _, up, down = estimation(s(distribution))(
                    process, region.varied(efficiency_filter))
                if up is not None and down is not None:
                    systs_passed_up[name].append(up)
                    systs_passed_down[name].append(down)
                else:
                    raise RuntimeError('something went wrong when applying '
                                       'systematic variation ' + s.name)
            else:
                systs_total_up[name].append(nominal_total)
                systs_total_down[name].append(nominal_total)
                systs_passed_up[name].append(nominal_passed)
                systs_passed_down[name].append(nominal_passed)

            #if not parallel.capturing():
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

        data_subtracted_total_test = data_total - background_total
        data_subtracted_passed_test = data_passed - background_passed

        # Compute the efficiencies
        data_efficiency_up.append(efficiency(data_subtracted_total_down,
                                             data_subtracted_passed_up))
        data_efficiency_down.append(efficiency(data_subtracted_total_up,
                                               data_subtracted_passed_down))
        normalize_efficiencies(data_efficiency,
                               data_efficiency_up[-1],
                               data_efficiency_down[-1])

        data_efficiency_up[-1].SetTitle(name + '_UP')
        data_efficiency_down[-1].SetTitle(name + '_DOWN')

        # Compute the offsets in the total yields and write out the
        # difference in yields *AFTER* having computed the efficiencies. (The
        # efficiency calculation sanitizes the graphs so that there are no
        # negative points, etc.)
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

    write_total_syst('total',
                     integral(data_subtracted_total),
                     sum_quadrature(total_offset_up),
                     sum_quadrature(total_offset_down))
    write_total_syst('passed',
                     integral(data_subtracted_passed),
                     sum_quadrature(passed_offset_up),
                     sum_quadrature(passed_offset_down))

    return data_efficiency, signal_efficiency, \
            data_efficiency_up, data_efficiency_down

def get_error(graph, zeroed = False):
    errors = graph.Clone(uuid4().hex)
    for i,x in zip(range(errors.GetN()), errors.GetX()):
        errors.SetPoint(i, x, 0.0)
    if zeroed:
        for i in range(errors.GetN()):
            errors.SetPointEYlow(i, 0.0)
            errors.SetPointEYhigh(i, 0.0)
    return errors

def set_error(graph, errors):
    if graph.GetN() != errors.GetN():
        raise RuntimeError('point count mismatch; '
                           'can\'t set errors from {} on {}'. \
                           format(errors.GetTitle, graph.GetTitle()))
    for i in range(graph.GetN()):
        graph.SetPointEYlow(i, errors.GetErrorYlow(i))
        graph.SetPointEYhigh(i, errors.GetErrorYhigh(i))

def flip_error(errors):
    flipped = errors.Clone(uuid4().hex)
    for i in range(errors.GetN()):
        flipped.SetPointEYlow(i, errors.GetErrorYhigh(i))
        flipped.SetPointEYhigh(i, errors.GetErrorYlow(i))
    return flipped

def clear_error(graph, y_only = False):
    for i in range(graph.GetN()):
        if not y_only:
            graph.SetPointEXlow(i, 0)
            graph.SetPointEXhigh(i, 0)
        graph.SetPointEYlow(i, 0)
        graph.SetPointEYhigh(i, 0)

def combine_errors(*errors):
    for e in errors[1:]:
        if errors[0].GetN() != e.GetN():
            raise RuntimeError('point count mismatch; '
                               'can\'t combine errors from {} with {}'. \
                               format(errors[0].GetTitle, e.GetTitle()))
    total = errors[0].Clone(uuid4().hex)
    for i in range(total.GetN()):
        total.SetPointEYlow(i, sum_quadrature([e.GetErrorYlow(i)
                                               for e
                                               in errors]))
        total.SetPointEYhigh(i, sum_quadrature([e.GetErrorYhigh(i)
                                                for e
                                                in errors]))
    return total

def compute_syst_error(nominal, up_variations, down_variations):
    if any([nominal.GetN() != v.GetN()
            for v
            in up_variations + down_variations]):
        raise RuntimeError('point count mismatch; '
                           'one or more of the variations don\'t agree '
                           'with the nominal.')

    y_nominal = nominal.GetY()
    y_up_variations = [e.GetY() for e in up_variations]
    y_down_variations = [e.GetY() for e in down_variations]

    errors = get_error(nominal, zeroed = True)
    for i in range(errors.GetN()):
        up_error = sum_quadrature([y_nominal[i] - y_variation[i]
                                   for y_variation
                                   in y_up_variations])
        down_error = sum_quadrature([y_nominal[i] - y_variation[i]
                                     for y_variation
                                     in y_down_variations])
        errors.SetPointEYhigh(i, up_error)
        errors.SetPointEYlow(i, down_error)
    return errors

def plot_efficiencies(data_efficiency,
                      data_syst_uncertainty,
                      signal_efficiency,
                      scale_factor,
                      scale_factor_uncertainties,
                      distribution,
                      path,
                      file_name_components,
                      label):
    data_syst_uncertainty_style = (kBlue-3, kBlue-3, 0)
    data_stat_uncertainty_style = (kCyan-7, kCyan-7, 0)
    signal_stat_uncertainty_style = (kRed, kRed, 0)

    data_stat_uncertainty = get_error(data_efficiency)
    data_total_uncertainty = combine_errors(data_stat_uncertainty,
                                            data_syst_uncertainty)

    syst_uncertainty_band = data_efficiency.Clone(uuid4().hex)
    syst_uncertainty_band.SetTitle('Data Syst.')
    set_error(syst_uncertainty_band, data_syst_uncertainty)

    #stat_uncertainty_band = data_efficiency.Clone(uuid4().hex)
    #stat_uncertainty_band.SetTitle('Data Stat.')
    #set_error(stat_uncertainty_band, data_stat_uncertainty)

    total_uncertainty_band = data_efficiency.Clone(uuid4().hex)
    total_uncertainty_band.SetTitle('Data Stat. #otimes Syst.')
    set_error(total_uncertainty_band, data_total_uncertainty)

    data_efficiency = data_efficiency.Clone(uuid4().hex)
    data_efficiency.SetTitle('Data')
    clear_error(data_efficiency)

    # Create the plot
    plot = Plot('', distribution.x_label(), 'Efficiency', ratio='True')

    plot.draw(
        #(stat_uncertainty_band, data_stat_uncertainty_style, 'e2'),
        (total_uncertainty_band, data_stat_uncertainty_style, 'e2'),
        (syst_uncertainty_band, data_syst_uncertainty_style, 'e2'),
        (signal_efficiency, default_red, 'ep'),
        (data_efficiency, default_black, 'p'),
    )

    sf_data_syst, sf_data_stat, sf_signal_stat = scale_factor_uncertainties

    # TODO: Not sure this is the way to present the uncertainties
    sf = scale_factor.Clone(uuid4().hex)
    clear_error(sf)

    sf_data_syst_band = scale_factor.Clone(uuid4().hex)
    sf_data_syst_band .SetTitle('Data Syst.')
    set_error(sf_data_syst_band, sf_data_syst)

    sf_signal_stat_band = scale_factor.Clone(uuid4().hex)
    sf_signal_stat_band .SetTitle('Data Syst. #otimes Data Stat. '
                                  '#otimes Signal Stat.')
    set_error(sf_signal_stat_band, combine_errors(sf_data_syst,
                                                  sf_signal_stat))

    sf_data_stat_band = scale_factor.Clone(uuid4().hex)
    sf_data_stat_band .SetTitle('Data Syst. #otimes Data Stat.')
    set_error(sf_data_stat_band, combine_errors(sf_data_syst,
                                                  sf_signal_stat,
                                                  sf_data_stat))

    plot.draw_ratios(
        (
            (sf_data_stat_band, data_stat_uncertainty_style, 'e2'),
            (sf_signal_stat_band, signal_stat_uncertainty_style, 'e2'),
            (sf_data_syst_band, data_syst_uncertainty_style, 'e2'),
            (sf, default_black, 'p')
        ),
        y_range = (0.8, 1.2),
        y_title = 'Scale Factor'
    )

    # Draw a legend
    plot.draw_legend(legend_entries = (signal_efficiency,
                                      data_efficiency,
                                      syst_uncertainty_band,
                                      #stat_uncertainty_band,
                                      total_uncertainty_band,
                                      ))

    # Draw an ATLAS stamp
    plot.draw_atlas_label(custom_label = label,
                          atlas_label = ATLAS_LABEL)

    plot.save(join(path, '_'.join(file_name_components)),
              arguments.extensions)

def do_scale_factor(data_efficiency,
                    data_efficiency_up,
                    data_efficiency_down,
                    signal_efficiency):
    def compute_sf(data_efficiency, signal_efficiency):
        sf = data_efficiency.Clone(uuid4().hex)
        for i,x,nom,denom in zip(range(sf.GetN()),
                                 sf.GetX(),
                                 data_efficiency.GetY(),
                                 signal_efficiency.GetY()):
            sf.SetPoint(i, x, nom/denom)
            sf.SetPointEYlow(i, 0.0)
            sf.SetPointEYhigh(i, 0.0)
        return sf

    def normalize_stat_error(efficiency):
        errors = get_error(efficiency)
        for i,low,high,y in zip(range(errors.GetN()),
                                errors.GetEYlow(),
                                errors.GetEYhigh(),
                                efficiency.GetY()):
            try:
                errors.SetPointEYlow(i, low/y)
            except ZeroDivisionError:
                errors.SetPointEYlow(i, 0.0)
            try:
                errors.SetPointEYhigh(i, high/y)
            except ZeroDivisionError:
                errors.SetPointEYhigh(i, 0.0)

        return errors

    ##############################################################
    # COMPUTE SCALE FACTORS
    ##############################################################
    nominal = compute_sf(data_efficiency, signal_efficiency)

    up_variations = [compute_sf(up, signal_efficiency)
                     for up
                     in data_efficiency_up]
    down_variations = [compute_sf(down, signal_efficiency)
                     for down
                     in data_efficiency_down]

    syst_uncertainty = compute_syst_error(nominal,
                                          up_variations,
                                          down_variations)
    syst_uncertainty.SetTitle('SYST')

    data_stat_uncertainty = normalize_stat_error(data_efficiency)
    data_stat_uncertainty.SetTitle('DATA STAT')

    signal_stat_uncertainty = flip_error(normalize_stat_error(signal_efficiency))
    signal_stat_uncertainty.SetTitle('SIGNAL STAT')

    set_error(nominal, combine_errors(syst_uncertainty,
                                      data_stat_uncertainty,
                                      signal_stat_uncertainty))
    nominal.SetTitle('Data / MC')

    return nominal, (syst_uncertainty,
                     data_stat_uncertainty,
                     signal_stat_uncertainty)


# NOTE: Keep this if we want to plot scale factors separately
#def plot_scale_factor(scale_factor,
                      #uncertainties,
                      #distribution,
                      #path,
                      #file_name_components,
                      #label):
    ## Compute the plot output path
    #save_path = join(path,
            #'_'.join(file_name_components + ['sf']))

    #plot([(scale_factor, default_black, 'ep')],
         #save_path,
         #x_label = distribution.x_label(),
         #y_label = 'Scale Factor',
         #custom_label = label,
         #atlas_label = ATLAS_LABEL,
         #extensions = arguments.extensions)

def save_to_root(data_efficiency,
                 signal_efficiency,
                 variation_efficiencies,
                 scale_factor,
                 scale_factor_uncertainties,
                 file_name):
    root_file.cd()

    clone = data_efficiency.Clone(uuid4().hex)
    clone.SetName('_'.join(['eff', file_name, 'data']))
    clone.Write()

    clone = signal_efficiency.Clone(uuid4().hex)
    clone.SetName('_'.join(['eff', file_name, 'mc']))
    clone.Write()

    for eff in variation_efficiencies:
        clone = eff.Clone(uuid4().hex)
        clone.SetName('_'.join(['eff', file_name, clone.GetTitle()]))
        clone.Write()

    clone = scale_factor.Clone(uuid4().hex)
    clone.SetName('_'.join(['sf', file_name]))
    clone.Write()

    for uncertainty,name in zip(scale_factor_uncertainties,
                                ['SYST', 'DATA_STAT', 'SIGNAL_STAT']):
        clone = uncertainty.Clone(uuid4().hex)
        clone.SetName('_'.join(['sf', file_name, name]))
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
    if syst == 'TEST_SYST_SHAPE':
        print('nominal: {:.1f}'.format(nominal))
        print('up: {:.1f}'.format(up))
        print('down: {:.1f}'.format(down))
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

            # Compute and plot the scale factors
            scale_factor, scale_factor_uncertainties = \
                do_scale_factor(data_efficiency,
                                data_efficiency_up,
                                data_efficiency_down,
                                signal_efficiency)

            data_syst_uncertainty = compute_syst_error(data_efficiency,
                                                       data_efficiency_up,
                                                       data_efficiency_down)
            plot_efficiencies(data_efficiency,
                              data_syst_uncertainty,
                              signal_efficiency,
                              scale_factor,
                              scale_factor_uncertainties,
                              distribution,
                              base_path,
                              [eff_name],
                              label)

            #plot_scale_factor(scale_factor,
                              #scale_factor_uncertainties,
                              #distribution,
                              #base_path,
                              #[eff_name],
                              #label)


            # Save efficiencies and scale factors to a root file
            if arguments.root_output:
                save_to_root(data_efficiency,
                             signal_efficiency,
                             data_efficiency_up + data_efficiency_down,
                             scale_factor,
                             scale_factor_uncertainties,
                             eff_name)

if arguments.text_output:
    text_file.close()

if arguments.root_output:
    root_file.ls()
    root_file.Close()
