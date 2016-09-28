#!/usr/bin/env python
#encoding: utf-8

# System imports
import argparse
from os import makedirs
from os.path import join, exists
from collections import OrderedDict
from copy import deepcopy
from math import sqrt
from array import array
from uuid import uuid4
from itertools import product

from scipy.optimize import curve_fit

# Six imports
from six import itervalues, iteritems, iterkeys

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.utility import efficiency, add_histograms, integral, get_bins, \
        add_overflow_to_last_bin
from owls_hep.plotting import Plot, style_line
from owls_hep.variations import Filtered
from owls_hep.uncertainty import to_shape, sum_quadrature

# owls-mutau imports
from owls_mutau.variations import OneProng, ThreeProng
from owls_mutau.styling import default_black, default_red

# ROOT imports
from ROOT import TGraphAsymmErrors, TFile, SetOwnership, \
        kCyan, kBlue, kBlack, kRed

Plot.PLOT_LEGEND_LEFT = 0.55
Plot.PLOT_LEGEND_RIGHT = 1.0
Plot.PLOT_LEGEND_TOP = 0.88
Plot.PLOT_HEADER_HEIGHT = 500

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
parser.add_argument('-d',
                    '--distribution',
                    required = True,
                    help = 'the distribution to use for the efficiencies',
                    metavar = '<distribution>')
parser.add_argument('-g',
                    '--triggers',
                    nargs = '+',
                    help = 'the triggers to compute efficiencies for',
                    metavar = '<trigger>')
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
parser.add_argument('-p',
                    '--publish',
                    action = 'store_true',
                    help = 'make plots for publishing')
parser.add_argument('-l',
                    '--label',
                    nargs = '*',
                    help = 'items to add to the custom label',
                    metavar = '<items>')
parser.add_argument('-a',
                    '--atlas-label',
                    default = None,
                    help = 'the label to use for the ATLAS stamp',
                    metavar = '<atlas-label>')
parser.add_argument('--no-prong-separated',
                    action = 'store_false',
                    dest = 'prong_separated',
                    default = True,
                    help = 'don\'t do 1p/3p efficiencies')
parser.add_argument('--no-inclusive',
                    action = 'store_false',
                    dest = 'inclusive',
                    default = True,
                    help = 'don\'t do inclusive efficiency')
parser.add_argument('definitions',
                    nargs = '*',
                    help = 'definitions to use within modules in the form x=y',
                    metavar = '<definition>')
arguments = parser.parse_args()


# Style for tau triger public plots
if arguments.publish:
    Plot.PLOT_MARGINS_WITH_RATIO = (0.125, 0.025, 0.025, 0.025)
    Plot.PLOT_RATIO_MARGINS = (0.125, 0.025, 0.325, 0.04)
    Plot.PLOT_HEADER_HEIGHT = 450 # px
    Plot.PLOT_LEGEND_TOP_WITH_RATIO = 0.95
    Plot.PLOT_LEGEND_LEFT = 0.62
    Plot.PLOT_LEGEND_TEXT_SIZE_WITH_RATIO = 0.055
    Plot.PLOT_LEGEND_ROW_SIZE_WITH_RATIO = 0.08
    Plot.PLOT_ATLAS_STAMP_TOP_WITH_RATIO = 0.88
    Plot.PLOT_ATLAS_STAMP_LEFT = 0.18
    Plot.PLOT_ATLAS_STAMP_TEXT_SIZE_WITH_RATIO = 0.065
    # Plot.PLOT_RATIO_Y_AXIS_NDIVISIONS = 404

# Parse definitions
definitions = dict((d.split('=') for d in arguments.definitions))


# Load files
model_file = load_module(arguments.model_file, definitions)
regions_file = load_module(arguments.regions_file, definitions)
distributions_file = load_module(arguments.distributions_file, definitions)
environment_file = load_module(arguments.environment_file, definitions)

# Extract model, region, and distribution
model = getattr(model_file, arguments.model)
region = getattr(regions_file, arguments.region)
distribution = getattr(distributions_file, arguments.distribution)
luminosity = model['luminosity']
sqrt_s = model['sqrt_s']
data = model['data']
signals = model['signals']
backgrounds = model['backgrounds']

available_triggers = regions_file.available_tau_triggers
systematics = model_file.osss_uncertainties

one_prong = region.varied(OneProng())
three_prong = region.varied(ThreeProng())

efficiencies = OrderedDict()

for name in arguments.triggers:
    try:
        trigger = available_triggers[name]
    except:
        raise KeyError('{} is not among the available triggers'.format(name))

    if arguments.inclusive:
        efficiencies[name] = {
            'label': trigger[2],
            'region': region,
            # 'title': '1+3-prong',
            'title': None,
            'rqcd_addons': ('', '_tau25'),
            'filter': Filtered('{} && {}'.format(*trigger))
        }

    if arguments.prong_separated:
        efficiencies[name + '_1p'] = {
            'label': trigger[2],
            'region': one_prong,
            'title': '1-prong',
            'rqcd_addons': ('_1p', '_tau25_1p'),
            'filter': Filtered('{} && {}'.format(*trigger))
        }

        efficiencies[name + '_3p'] = {
            'label': trigger[2],
            'region': three_prong,
            'title': '3-prong',
            'rqcd_addons': ('_3p', '_tau25_3p'),
            'filter': Filtered('{} && {}'.format(*trigger))
        }


# Get computation environment
cache = getattr(environment_file, 'persistent_cache', None)
backend = getattr(environment_file, 'parallelization_backend', None)

# Create the parallelization environment
parallel = ParallelizedEnvironment(backend)

# Create the directories for the different processes
base_path = arguments.output
if not exists(base_path):
    makedirs(base_path)

print('Script options')
print('  Output directory: {}'.format(base_path))
print('  Data prefix: {}'.format(definitions.get('data_prefix', 'UNDEFINED')))
print('  Model file: {}'.format(arguments.model_file))
print('  Region file: {}'.format(arguments.regions_file))
print('  Systematics treatment: {}'.format(model_file.systematics))
print('  Region: {}'.format(arguments.region))
print('  Distribution: {}'.format(arguments.distribution))
print('  Triggers: {}'.format(', '.join(arguments.triggers)))

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
            print('  Switching {:.5f} and {:.5f}'.format(y_up, y_down))
            y_up, y_down = y_down, y_up

        # If up variation is lower than nominal, reset
        if y_up < y:
            print('  Resetting {:.5f} < {:.5f}'.format(y_up, y))
            y_up = y

        # If down variation is greater than nominal, reset
        if y_down > y:
            print('  Resetting {:.5f} > {:.5f}'.format(y_down, y))
            y_down = y

        up.SetPoint(i, x, y_up)
        down.SetPoint(i, x, y_down)

def do_efficiencies(distribution, region, rqcd_addons, efficiency_filter):
    ##############################################################
    # COMPUTE (DATA-BACKGROUND) AND SIGNAL HISTOGRAMS
    ##############################################################
    process = data['process']
    estimation = data['estimation']

    # Prepare the region
    total_region = deepcopy(region)
    passed_region = region.varied(efficiency_filter)
    total_region.metadata()['rqcd'] += rqcd_addons[0]
    passed_region.metadata()['rqcd'] += rqcd_addons[1]

    # Compute the total and passed histograms
    data_total = estimation(distribution)(process, total_region)
    data_passed = estimation(distribution)(process, passed_region)
    add_overflow_to_last_bin(data_total)
    add_overflow_to_last_bin(data_passed)

    backgrounds_total = []
    backgrounds_passed = []
    for background in itervalues(backgrounds):
        # Extract parameters
        process = background['process']
        estimation = background['estimation']

        # Compute the total and passed histograms
        backgrounds_total.append(
            estimation(distribution)(process, total_region)
        )
        backgrounds_passed.append(
            estimation(distribution)(process, passed_region)
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
            estimation(distribution)(process, total_region)
        )
        signals_passed.append(
            estimation(distribution)(process, passed_region)
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

            nominal_total = estimation(distribution)(process, total_region)
            nominal_passed = estimation(distribution)(process, passed_region)

            if s in uncertainties:
                # Get the up/down of the total
                _, _, up, down = estimation(s(distribution))(process,
                                                             total_region)
                if up is not None and down is not None:
                    systs_total_up[name].append(up)
                    systs_total_down[name].append(down)
                else:
                    raise RuntimeError('something went wrong when applying '
                                       'systematic variation ' + s.name)

                # Get the up/down of the passed
                _, _, up, down = estimation(s(distribution))(process,
                                                             passed_region)
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
    add_overflow_to_last_bin(signal_total)
    add_overflow_to_last_bin(signal_passed)
    signal_efficiency = efficiency(signal_total, signal_passed)
    signal_efficiency.SetTitle('MC')


    ##############################################################
    # COMPUTE NOMINAL DATA EFFICIENCY
    ##############################################################
    background_total = add_histograms(backgrounds_total, 'Bkg')
    background_passed = add_histograms(backgrounds_passed, 'Bkg')

    add_overflow_to_last_bin(background_total)
    add_overflow_to_last_bin(background_passed)

    data_subtracted_total = data_total - background_total
    data_subtracted_passed = data_passed - background_passed

    data_efficiency = efficiency(data_subtracted_total, data_subtracted_passed)
    data_efficiency.SetTitle(data['process'].label())

    # Write the signal and data counts
    write_counts('Signal total/passed', signal_total, signal_passed)
    write_counts('Data total/passed', data_total, data_passed)
    write_counts('Data-bkg total/passed',
                 data_subtracted_total,
                 data_subtracted_passed)
    write_bins('Total', signal_total, data_total,
               background_total, data_subtracted_total)
    write_bins('Passed', signal_passed, data_passed,
               background_passed, data_subtracted_passed)

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
        add_overflow_to_last_bin(syst_total_up)
        add_overflow_to_last_bin(syst_passed_up)
        data_subtracted_total_down = data_total - syst_total_up
        data_subtracted_passed_down = data_passed - syst_passed_up

        syst_total_down = add_histograms(systs_total_down[name], 'Bkg')
        syst_passed_down = add_histograms(systs_passed_down[name], 'Bkg')
        add_overflow_to_last_bin(syst_total_down)
        add_overflow_to_last_bin(syst_passed_down)
        data_subtracted_total_up = data_total - syst_total_down
        data_subtracted_passed_up = data_passed - syst_passed_down

        # Write out the resulting histograms
        write_binned_syst('{}-TOTAL'.format(name),
                          data_total,
                          data_subtracted_total,
                          data_subtracted_total_up,
                          data_subtracted_total_down)
        write_binned_syst('{}-PASSED'.format(name),
                          data_passed,
                          data_subtracted_passed,
                          data_subtracted_passed_up,
                          data_subtracted_passed_down)

        # Compute the efficiencies
        if name in ['RQCD_STAT', 'RQCD_SYST']:
            print('Using uncorrelated systematics for {}'.format(name))
            up = efficiency(data_subtracted_total_down,
                            data_subtracted_passed)
            down = efficiency(data_subtracted_total_up,
                              data_subtracted_passed)
            normalize_efficiencies(data_efficiency, up, down)
            up.SetTitle(name + '_UP_TOTAL')
            down.SetTitle(name + '_DOWN_TOTAL')
            data_efficiency_up.append(up)
            data_efficiency_down.append(down)

            up = efficiency(data_subtracted_total,
                            data_subtracted_passed_up)
            down = efficiency(data_subtracted_total,
                              data_subtracted_passed_down)
            normalize_efficiencies(data_efficiency, up, down)
            up.SetTitle(name + '_UP_PASSED')
            down.SetTitle(name + '_DOWN_PASSED')
            data_efficiency_up.append(up)
            data_efficiency_down.append(down)

        else:
            print('Using correlated systematics for {}.'.format(name))
            # NOTE: Reversed up/down results in fewer switches
            down = efficiency(data_subtracted_total_up,
                              data_subtracted_passed_up)
            up = efficiency(data_subtracted_total_down,
                            data_subtracted_passed_down)
            normalize_efficiencies(data_efficiency, up, down)
            up.SetTitle(name + '_UP')
            down.SetTitle(name + '_DOWN')
            data_efficiency_up.append(up)
            data_efficiency_down.append(down)

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
    write_efficiency(signal_efficiency, data_efficiency)

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
    total_uncertainty_band.SetTitle('Data Stat. #oplus Syst.')
    set_error(total_uncertainty_band, data_total_uncertainty)

    data_efficiency = data_efficiency.Clone(uuid4().hex)
    # data_efficiency.SetTitle('Data')
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
    sf_data_syst_band.SetTitle('Data Syst.')
    set_error(sf_data_syst_band, sf_data_syst)

    sf_signal_stat_band = scale_factor.Clone(uuid4().hex)
    sf_signal_stat_band.SetTitle('Data Syst. #oplus Signal Stat.')
    set_error(sf_signal_stat_band, combine_errors(sf_data_syst,
                                                  sf_signal_stat))

    sf_data_stat_band = scale_factor.Clone(uuid4().hex)
    sf_signal_stat_band.SetTitle('Data Syst. #oplus Data Stat. '
                                 '#oplus Signal Stat.')
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
        y_range = (0.5, 1.5),
        # y_title = 'Scale Factor'
        y_title = 'Data / exp.'
    )

    # Draw a legend
    plot.draw_legend(legend_entries = (signal_efficiency,
                                      data_efficiency,
                                      syst_uncertainty_band,
                                      #stat_uncertainty_band,
                                      total_uncertainty_band,
                                      ))

    # Draw an ATLAS stamp
    plot.draw_atlas_label(luminosity,
                          sqrt_s,
                          custom_label = label,
                          atlas_label = arguments.atlas_label)

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
            try:
                sf.SetPoint(i, x, nom/denom)
            except ZeroDivisionError:
                sf.SetPoint(i, x, 0.0)
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

    # TODO: The statistical errors are normalized to 1, but perhaps they
    # should be normalized to the SF instead? I.e. that we should supply
    # nominal to normalize_stat_error and do low = eff_low/eff_y * sf_y. I'm
    # not sure that is correct.
    data_stat_uncertainty = normalize_stat_error(data_efficiency)
    data_stat_uncertainty.SetTitle('DATA STAT')

    signal_stat_uncertainty = flip_error(normalize_stat_error(signal_efficiency))
    signal_stat_uncertainty.SetTitle('SIGNAL STAT')

    set_error(nominal, combine_errors(syst_uncertainty,
                                      data_stat_uncertainty,
                                      signal_stat_uncertainty))
    nominal.SetTitle('Data / exp.')

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
         #atlas_label = arguments.atlas_label,
         #extensions = arguments.extensions)

def get_weighted_efficiency(centres, efficiencies, weights):
    # Constant function for regression
    def const_func(x, a):
        return a
    # Perform the regression
    popt, _ = curve_fit(const_func, centres, efficiencies, sigma = weights)
    # popt is a list of curve fit parameters; we're only interested in the
    # constant term (a)
    return popt[0]

def get_weighted_uncertainty_efficiencies(centres,
                                          nominal,
                                          weights,
                                          uncertainty):
    nominal_up = [y+e for y, e in zip(nominal, uncertainty.GetEYhigh())]
    nominal_down = [y-e for y, e in zip(nominal, uncertainty.GetEYlow())]
    weighted_up = get_weighted_efficiency(centres, nominal_up, weights)
    weighted_down = get_weighted_efficiency(centres, nominal_down, weights)
    return (weighted_up, weighted_down)

def estimate_systematic_effects(data_efficiency,
                                data_efficiency_up,
                                data_efficiency_down):
    n = data_efficiency.GetN()
    centres = [x for i, x in zip(range(n), data_efficiency.GetX())]
    efficiencies = [x for i, x in zip(range(n), data_efficiency.GetY())]
    stat_up = [x for i, x in zip(range(n), data_efficiency.GetEYhigh())]
    stat_down = [x for i, x in zip(range(n), data_efficiency.GetEYlow())]
    # Average uncertainty
    # weights = [((u + d)/2)
               # for i, u, d
               # in zip(range(n), stat_up, stat_down)]
    # Largest uncertainty
    weights = [max(u, d)
               for i, u, d
               in zip(range(n), stat_up, stat_down)]

    weighted_efficiency = \
            get_weighted_efficiency(centres, efficiencies, weights)


    rqcd_variations = ([u for u in data_efficiency_up
                        if 'RQCD' in u.GetTitle()],
                       [u for u in data_efficiency_down
                        if 'RQCD' in u.GetTitle()])
    bjet_variations = ([u for u in data_efficiency_up
                        if 'BJET' in u.GetTitle()],
                       [u for u in data_efficiency_down
                        if 'BJET' in u.GetTitle()])
    prw_variations = ([u for u in data_efficiency_up
                       if 'PRW' in u.GetTitle()],
                      [u for u in data_efficiency_down
                       if 'PRW' in u.GetTitle()])
    muon_variations = ([u for u in data_efficiency_up
                        if 'MUON' in u.GetTitle()],
                       [u for u in data_efficiency_down
                        if 'MUON' in u.GetTitle()])

    rqcd_uncertainty = compute_syst_error(data_efficiency, *rqcd_variations)
    bjet_uncertainty = compute_syst_error(data_efficiency, *bjet_variations)
    prw_uncertainty = compute_syst_error(data_efficiency, *prw_variations)
    muon_uncertainty = compute_syst_error(data_efficiency, *muon_variations)
    all_uncertainty = compute_syst_error(data_efficiency,
                                         data_efficiency_up,
                                         data_efficiency_down)

    # up = [y for x, y in zip(centres, all_uncertainty.GetEYhigh())]
    # down = [y for x, y in zip(centres, all_uncertainty.GetEYlow())]
    # print('ALL syst')
    # for x, y, u, d in zip(centres, efficiencies, up, down):
        # print('{:5.1f} {:.3f}({:.3f}↓ {:.3f}↑)'.format(x, y, d, u))

    # up = [y for x, y in zip(centres, rqcd_uncertainty.GetEYhigh())]
    # down = [y for x, y in zip(centres, rqcd_uncertainty.GetEYlow())]
    # print('RQCD syst')
    # for x, y, u, d in zip(centres, efficiencies, up, down):
        # print('{:5.1f} {:.3f}({:.3f}↓ {:.3f}↑)'.format(x, y, d, u))

    # up = [y for x, y in zip(centres, prw_uncertainty.GetEYhigh())]
    # down = [y for x, y in zip(centres, prw_uncertainty.GetEYlow())]
    # print('PRW syst')
    # for x, y, u, d in zip(centres, efficiencies, up, down):
        # print('{:5.1f} {:.3f}({:.3f}↓ {:.3f}↑)'.format(x, y, d, u))

    rqcd_efficiencies = get_weighted_uncertainty_efficiencies(centres,
                                                              efficiencies,
                                                              weights,
                                                              rqcd_uncertainty)
    bjet_efficiencies = get_weighted_uncertainty_efficiencies(centres,
                                                              efficiencies,
                                                              weights,
                                                              bjet_uncertainty)
    prw_efficiencies = get_weighted_uncertainty_efficiencies(centres,
                                                              efficiencies,
                                                              weights,
                                                              prw_uncertainty)
    muon_efficiencies = get_weighted_uncertainty_efficiencies(centres,
                                                              efficiencies,
                                                              weights,
                                                              muon_uncertainty)
    all_efficiencies = get_weighted_uncertainty_efficiencies(centres,
                                                             efficiencies,
                                                             weights,
                                                             all_uncertainty)

    rqcd_effects = tuple([abs((x - weighted_efficiency)/weighted_efficiency)
                          for x in rqcd_efficiencies])
    bjet_effects = tuple([abs((x - weighted_efficiency)/weighted_efficiency)
                          for x in bjet_efficiencies])
    prw_effects = tuple([abs((x - weighted_efficiency)/weighted_efficiency)
                          for x in prw_efficiencies])
    muon_effects = tuple([abs((x - weighted_efficiency)/weighted_efficiency)
                          for x in muon_efficiencies])
    all_effects = tuple([abs((x - weighted_efficiency)/weighted_efficiency)
                         for x in all_efficiencies])

    if arguments.text_output:
        text_file.write('--- Systematic uncertainties bin-by-bin (syst. unc.) ---\n')
        for i, x, e, u, d in zip(range(n),
                                 centres,
                                 efficiencies,
                                 all_uncertainty.GetEYhigh(),
                                 all_uncertainty.GetEYlow()):
            text_file.write('{:4d} ({:5.1f}, {:5.3f}(↓{:5.3f}↑{:5.3f})) '
                            '{:.3f}%\n'. \
                            format(i, x, e, u, d, max(u, d)/e*100))
        text_file.write('--- Weighted averages (syst. unc.) ---\n')
        text_file.write('Weighted efficiency: {:.3f}\n'. \
                        format(weighted_efficiency))
        text_file.write('RQCD up/down:  {:.3f}/{:.3f} ({:.3f}%)\n'. \
                        format(rqcd_efficiencies[0],
                               rqcd_efficiencies[1],
                               max(*rqcd_effects)*100))
        text_file.write('BJET up/down:  {:.3f}/{:.3f} ({:.3f}%)\n'. \
                        format(bjet_efficiencies[0],
                               bjet_efficiencies[1],
                               max(*bjet_effects)*100))
        text_file.write('PRW up/down:   {:.3f}/{:.3f} ({:.3f}%)\n'. \
                        format(prw_efficiencies[0],
                               prw_efficiencies[1],
                               max(*prw_effects)*100))
        text_file.write('MUON up/down:  {:.3f}/{:.3f} ({:.3f}%)\n'. \
                        format(muon_efficiencies[0],
                               muon_efficiencies[1],
                               max(*muon_effects)*100))
        text_file.write('TOTAL up/down: {:.3f}/{:.3f} ({:.3f}%)\n'. \
                        format(all_efficiencies[0],
                               all_efficiencies[1],
                               max(*all_effects)*100))




def save_to_root(data_efficiency,
                 signal_efficiency,
                 data_syst_uncertainty,
                 variation_efficiencies,
                 scale_factor,
                 scale_factor_uncertainties,
                 file_name):
    root_file.cd()

    # NOTE: The statistical uncertainties on the efficiencies are attached to
    # the graphs
    clone = data_efficiency.Clone(uuid4().hex)
    clone.SetName('_'.join(['eff', file_name, 'data']))
    clone.Write()

    clone = signal_efficiency.Clone(uuid4().hex)
    clone.SetName('_'.join(['eff', file_name, 'mc']))
    clone.Write()

    clone = data_syst_uncertainty.Clone(uuid4().hex)
    clone.SetName('_'.join(['eff', file_name, 'SYST']))
    clone.SetTitle(clone.GetTitle() + ' SYST')
    clone.Write()

    # NOTE: The individual syst uncertainties are not that useful.
    # for eff in variation_efficiencies:
        # clone = eff.Clone(uuid4().hex)
        # clone.SetName('_'.join(['eff', file_name, clone.GetTitle()]))
        # clone.Write()

    clone = scale_factor.Clone(uuid4().hex)
    clone.SetName('_'.join(['sf', file_name]))
    clone.Write()

    for uncertainty,name in zip(scale_factor_uncertainties,
                                ['SYST', 'DATA_STAT', 'SIGNAL_STAT']):
        clone = uncertainty.Clone(uuid4().hex)
        clone.SetName('_'.join(['sf', file_name, name]))
        clone.Write()
    clone = combine_errors(scale_factor_uncertainties[1],
                           scale_factor_uncertainties[2])
    clone.SetName('_'.join(['sf', file_name, 'STAT']))
    clone.SetTitle('_'.join(['sf', file_name, 'STAT']))
    clone.Write()

def write_counts(message, total, passed):
    if arguments.text_output:
        text_file.write('{}: {:.1f}/{:.1f}\n'. \
                        format(message, integral(total), integral(passed)))

def write_bins(message, signal, data, background, data_subtracted):
    if arguments.text_output:
        text_file.write('{} bin-by-bin\n'.format(message))
        text_file.write('{:3s} ({:7s}, {:12s} {:12s} {:12s} {:12s})\n'.\
              format('Bin', 'Centre', 'Signal', 'Data', 'Background', 'Data-Bkg'))
        for i in range(signal.GetNbinsX()):
            text_file.write('{:3d} ({:6.1f}, {:6.1f}±{:4.1f} {:6.1f}±{:4.1f} '
                            '{:6.1f}±{:4.1f} {:6.1f}±{:4.1f})\n'.\
                            format(i,
                                   signal.GetBinCenter(i+1),
                                   signal.GetBinContent(i+1),
                                   signal.GetBinError(i+1),
                                   data.GetBinContent(i+1),
                                   data.GetBinError(i+1),
                                   background.GetBinContent(i+1),
                                   background.GetBinError(i+1),
                                   data_subtracted.GetBinContent(i+1),
                                   data_subtracted.GetBinError(i+1)))


def write_binned_syst(what, raw, nominal, up, down):
    if arguments.text_output:
        text_file.write('--- {} ---\n'.format(what))
        for i, (rx, ry), (nx, ny), (ux, uy), (dx, dy) \
                in zip(range(nominal.GetNbinsX()+2),
                       get_bins(raw, True),
                       get_bins(nominal, True),
                       get_bins(up, True),
                       get_bins(down, True)):
            text_file.write('{:4d} ({:5.1f}, {:6.1f}r {:6.1f}n '
                            '{:6.1f}↑ {:6.1f}↓)\n'.
                            format(i, rx, ry, ny, uy, dy))

def write_total_syst(what, nominal_count, up_offset, down_offset):
    if arguments.text_output:
        text_file.write('{:30s} {:10s}: {:6.1f} ({:5.2f}%) | {:6.1f} | '
                        '{:6.1f} ({:5.2f}%)\n'. \
                        format('ALL',
                               what,
                               nominal_count - down_offset,
                               -down_offset / nominal_count * 100.0,
                               nominal_count,
                               nominal_count + up_offset,
                               up_offset / nominal_count * 100.0))

def write_efficiency(signal, data):
    if arguments.text_output:
        text_file.write('--- Efficiency (stat. unc.) ---\n')
        x = signal.GetX()
        signal_y = signal.GetY()
        signal_yel = signal.GetEYlow()
        signal_yeh = signal.GetEYhigh()
        data_y = data.GetY()
        data_yel = data.GetEYlow()
        data_yeh = data.GetEYhigh()

        text_file.write('      {:>5s}  {:18s}  {:18s}\n'. \
                        format('pT', 'Signal (MC)', 'Data-bkg'))
        for i in range(signal.GetN()):
            text_file.write('{:4d} ({:5.1f}, {:5.3f}(↓{:5.3f}↑{:5.3f}) '
                            '{:5.3f}(↓{:5.3f}↑{:5.3f}))\n'. \
                            format(i, x[i],
                                   signal_y[i], signal_yel[i], signal_yeh[i],
                                   data_y[i], data_yel[i], data_yeh[i]))

def write_counts_background(syst, what, nominal, up, down):
    def percentage(var):
        return (var/nominal - 1.0) * 100.0
    if arguments.text_output:
        nominal, up, down = integral(nominal), integral(up), integral(down)
        if syst == 'TEST_SYST_SHAPE':
            print('nominal: {:.1f}'.format(nominal))
            print('up: {:.1f}'.format(up))
            print('down: {:.1f}'.format(down))
        pc_up, pc_down = percentage(up), percentage(down)
        text_file.write('{:30s} {:10s}: {:6.1f} ({:5.2f}%) | {:6.1f} | '
                        '{:6.1f} ({:5.2f}%)\n'. \
                        format(syst, what, down, pc_down, nominal, up, pc_up))

def open_files(path, file_name_components):
    # Open root file for output
    global root_file
    file_name = join(path, '{}.root'.format('_'.join(file_name_components)))
    if arguments.root_output:
        root_file =  TFile.Open(file_name, 'RECREATE')

    # Open text file for output
    global text_file
    file_name = join(path, '{}.txt'.format('_'.join(file_name_components)))
    if arguments.text_output:
        text_file =  open(file_name, 'w')

def close_files():
    if arguments.text_output:
        text_file.close()

    if arguments.root_output:
        root_file.ls()
        root_file.Close()

# Run in a cached environment
with caching_into(cache):

    # Run in a parallelized environment
    while parallel.run():
        if parallel.computed():
            print('Computing efficiencies...')

        for eff_name, eff in iteritems(efficiencies):
            open_files(base_path, [eff_name])
            efficiency_filter = eff['filter']
            region = eff['region']
            rqcd_addons = eff['rqcd_addons']

            if arguments.text_output and not parallel.capturing():
                text_file.write('Efficiencies for {}\n'.format(eff_name))

            label = region.label()
            if len(label) > 0:
                label[0] += ', {}'.format(eff['title'])
            else:
                label.append(eff['title'])
            label.append(eff['label'])

    ##############################################################
    # CREATE AND PLOT NOMINAL EFFICIENCIES AND SCALE FACTORS
    ##############################################################

            # Compute and plot the efficiencies
            data_efficiency, signal_efficiency, \
                    data_efficiency_up, data_efficiency_down = \
                    do_efficiencies(distribution,
                                    region,
                                    rqcd_addons,
                                    efficiency_filter)

            # If capturing at pass 1, the efficiencies are bogus, continue
            if parallel.capturing():
                continue

            # Estimate the effects of each systematic on the efficiency
            estimate_systematic_effects(data_efficiency,
                                        data_efficiency_up,
                                        data_efficiency_down)

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
                             data_syst_uncertainty,
                             data_efficiency_up + data_efficiency_down,
                             scale_factor,
                             scale_factor_uncertainties,
                             eff_name)
            close_files()

