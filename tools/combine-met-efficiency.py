#!/usr/bin/env python


# System imports
import argparse
from os import makedirs
from os.path import join, exists
from functools import partial
from uuid import uuid4
from array import array
from collections import OrderedDict
from types import FunctionType

# Six imports
from six import itervalues, iteritems, iterkeys

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.utility import load_file, clone, efficiency, get_bins
from owls_hep.plotting import Plot, enable_fit, style_line
from owls_hep.region import Region

# owls-taunu imports
from owls_taunu.taujets.variations import Triggered, Filtered
from owls_taunu.styling import line_black_thin, line_red_thin, \
        line_dashed_grey

# ROOT imports
from ROOT import TFormula, TF1, TFile, TLine, SetOwnership

Plot.PLOT_LEGEND_LEFT = 0.45
Plot.PLOT_LEGEND_RIGHT = 1.0
Plot.PLOT_LEGEND_TOP = 0.88
Plot.PLOT_LEGEND_TOP_WITH_RATIO = 0.85
Plot.PLOT_LEGEND_TEXT_SIZE = 0.045
Plot.PLOT_LEGEND_TEXT_SIZE_WITH_RATIO = 0.055
Plot.PLOT_HEADER_HEIGHT = 200
Plot.PLOT_RATIO_Y_AXIS_NDIVISIONS = 402

# Parse command line arguments
parser = argparse.ArgumentParser(
    description = 'Generate plots and a combined plotbook'
)
parser.add_argument('-o',
                    '--output',
                    default = 'plots',
                    help = 'the plot output directory',
                    metavar = '<output>')
parser.add_argument('-i',
                    '--input-file',
                    required = True,
                    help = 'the input file containing the efficiencies and '
                    'the fits',
                    metavar = '<input-file>')
parser.add_argument('-v',
                    '--variations',
                    nargs = '+',
                    help = 'variations for which to consider systematic '
                    'effects',
                    metavar = '<efficiency>')
parser.add_argument('--root-output',
                    action = 'store_true',
                    help = 'write total fits and systematic variation to a '
                    'ROOT file')
parser.add_argument('--cut-off',
                    nargs = '+',
                    default = None,
                    type = float,
                    help = 'cut-off where the efficiency is considered to be '
                    '100 %')
parser.add_argument('--cut-markers',
                    nargs = '+',
                    type = float,
                    help = 'draw a cut marker at the position on the '
                    'x-axis (default: off)')
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
input_file = load_file(arguments.input_file)

variations = [
    ('met_et_nomu_trig_mu_jets', 'mu_jets'),
    ('met_et_trig_e_medium', 'e_medium'),
    #('met_et_trig_e_tight', 'e_tight'),
    ('met_et_trig_stat', 'stat'),
    ('met_et_trig_tau_1p', 'tau_1p'),
    ('met_et_trig_tau_3p', 'tau_3p'),
    ('met_et_trig_tau_medium', 'tau_medium'),
    ('met_et_trig_3jets', '3jets'),
    #('met_et_trig_tau_tight', 'tau_tight'),
]

# Extract efficiencies to compute
if arguments.variations is not None:
    variations = [d for d in variations if d[0] in arguments.efficiencies]

fit_func_str = '[0]*(1.0 + TMath::Erf((x - [1])/[2])) + [3]'
fit_func_str2 = ('([0]*(1.0 + TMath::Erf((x - [1])/[2])) + [3]) * '
                 '([4]*(1.0 + TMath::Erf((x - [5])/[6])) + [7])')

# Create the directories for the different processes
base_path = arguments.output
if not exists(base_path):
    makedirs(base_path)

def eval_fit_divide(fit, nominal, x):
    try:
        # x is a PyDoubleBuffer containing (x, y, z, t)
        return fit.Eval(x[0]) / nominal.Eval(x[0])
    except ZeroDivisionError:
        return 1.0

def get_ratio(fit, nominal, x_range):
    divide = partial(eval_fit_divide, fit, nominal)
    ratio = TF1(uuid4().hex, divide, *x_range)
    return ratio

def eval_fit_multiply(left, right, x):
    # x is a PyDoubleBuffer containing (x, y, z, t)
    return left.Eval(x[0]) * right.Eval(x[0])

def get_product(root_file, l1_key, hlt_key, x_range):
    l1 = input_file.Get(l1_key)
    hlt = input_file.Get(hlt_key)
    multiply = partial(eval_fit_multiply, l1, hlt)
    product = TF1(uuid4().hex, multiply, *x_range)
    return product



def plot_product(nominal,
                 variation,
                 x_range,
                 x_label,
                 path,
                 file_name,
                 label = None):

    # Create the plot
    plot = Plot('',
                x_label,
                'Efficiency',
                ratio = (variation is not None))

    # Compose the efficiencies and the fits
    drawables_styles_options = [(nominal, line_black_thin, 'l')]
    if variation is not None:
        drawables_styles_options.append((variation, line_red_thin, 'l'))

    # Add an optional line
    if arguments.cut_markers is not None:
        for m in arguments.cut_markers:
            line = TLine(m, 0, m, 1.05)
            drawables_styles_options.append((line, line_dashed_grey, 'l'))

    # Draw the main pad
    plot.draw(*drawables_styles_options)

    if variation is not None:
        ratio = get_ratio(nominal, variation, x_range)

        ratio_y_range = (0.8, 1.2)
        ratio_y_label = '#frac{variation}{nominal}'

        drawables_styles_options = [(ratio, line_red_thin, 'l')]

        # Add an optional line
        if arguments.cut_markers is not None:
            for m in arguments.cut_markers:
                line = TLine(m, ratio_y_range[0], m, ratio_y_range[1])
                drawables_styles_options.append((line, line_dashed_grey, 'l'))

        plot.draw_ratios(drawables_styles_options,
                         y_range = ratio_y_range,
                         y_title = ratio_y_label)

    # Draw a legend
    plot.draw_legend(use_functions = True)

    # Draw an ATLAS stamp
    plot.draw_atlas_label(luminosity = None,
                          custom_label = label,
                          atlas_label = None)

    # Save the plot
    save_path = join(path, file_name)
    plot.save(save_path, arguments.extensions)


def save_to_root(src, name, root_file):
    root_file.cd()
    o = clone(src)
    o.SetName(name)
    o.Write()

############################################################
# MAIN SCRIPT
############################################################

# Compute the plot output path
if arguments.root_output:
    output_file =  TFile.Open(join(base_path, 'met_efficiencies_combined.root'),
                            'RECREATE')

print('Script options')
print('  Output directory: {}'.format(base_path))
print('  Input file: {}'.format(arguments.input_file))
if arguments.cut_off:
    print('  Cut off: {}'.format(arguments.cut_off))


nominal_eff = input_file.Get('eff_met_et_trig_nominal')
x_range = (nominal_eff.GetXaxis().GetXmin(), nominal_eff.GetXaxis().GetXmax())
x_label = nominal_eff.GetXaxis().GetTitle()
print('  Got x-range: {}'.format(x_range))
print('  Got x-label: {}'.format(x_label))

label = ['HLT_xe70', 'e_{loose}+jets+b+#tau_{loose}']

nominal_product = get_product(input_file,
                              'fit_met_et_trig_nominal_L1',
                              'fit_met_et_trig_nominal_L1_HLT',
                              x_range)
nominal_product.SetTitle('Nominal')
save_to_root(nominal_product, 'met_eff_nominal', output_file)
plot_product(nominal_product,
             None,
             x_range,
             x_label,
             base_path,
             'met_eff_nominal',
             label)


nominal_comp = input_file.Get('fit_met_et_trig_nominal')
#save_to_root(nominal_comp, 'met_eff_nominal_comp', output_file)
nominal_comp.SetTitle('#epsilon_{HLT only}')
nominal_product.SetTitle('Nominal (#epsilon_{L1} #times #epsilon_{HLT})')
plot_product(nominal_product,
             nominal_comp,
             x_range,
             x_label,
             base_path,
             'met_eff_nominal_comp',
             label)
nominal_product.SetTitle('Nominal')

for var,var_name in variations:
    var_eff = input_file.Get('eff_' + var)
    var_product = get_product(input_file,
                                    'fit_' + var + '_L1',
                                    'fit_' + var + '_L1_HLT',
                                    x_range)
    var_product.SetTitle(var_eff.GetTitle())
    save_to_root(var_product,
                 'met_eff_variation_' + var_name,
                 output_file)
    plot_product(nominal_product,
                 var_product,
                 x_range,
                 x_label,
                 base_path,
                 'met_eff_variation_' + var_name,
                 label)


if arguments.root_output:
    output_file.ls()
    output_file.Close()
