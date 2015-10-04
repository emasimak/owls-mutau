#!/usr/bin/env python


# System imports
import argparse
from os import makedirs
from os.path import join, exists, isdir
from itertools import product, chain
from math import sqrt

# Six imports
from six import itervalues
from six.moves import range

# owls-cache imports
from owls_cache.persistent import caching_into

# owls-parallel imports
from owls_parallel import ParallelizedEnvironment

# owls-hep imports
from owls_hep.module import load as load_module
from owls_hep.uncertainty import uncertainty_band, combined_uncertainty_band, \
    ratio_uncertainty_band
from owls_hep.plotting import Plot, histogram_stack, combined_histogram, \
    ratio_histogram


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
parser.add_argument('-t',
                    '--text-counts',
                    action = 'store_true',
                    help = 'enable text output of counts')
parser.add_argument('-n',
                    '--no-counts',
                    action = 'store_true',
                    help = 'disable event counts in legends')
parser.add_argument('-e',
                    '--error-label',
                    default = 'Stat. Unc.',
                    help = 'the label to use for error bands',
                    metavar = '<error-label>')
parser.add_argument('-s',
                    '--signal-scale',
                    default = 1.0,
                    type = float,
                    help = 'A scale factor for rendering signal',
                    metavar = '<signal-scale-factor>')
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
luminosity = model['luminosity']
sqrt_s = model['sqrt_s']
signals = model['signals']
backgrounds = model['backgrounds']
data = model['data']

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

# Create output directories
for region_name in regions:
    # Compute the region's output path
    region_path = join(arguments.output, region_name)

    # Try to create it
    if not exists(region_path):
        makedirs(region_path)


# Run in a cached environment
with caching_into(cache):
    # Run in a parallelized environment
    while parallel.run():
        if parallel.computed():
            print('Creating plots...')

        # Loop over regions and distributions
        for region_name, distribution_name in product(regions, distributions):
            # Grab the region/distribution objects
            region = regions[region_name]
            distribution = distributions[distribution_name]

            # Create the data histogram
            data_process = data['process']
            data_estimation = data['estimation']
            data_histogram = data_estimation(distribution)(
                data_process,
                region
            )
            data_histogram.SetTitle('Data')

            # If this region is blinded, then zero-out the data histogram
            if region.metadata().get('blinded', False):
                data_histogram.Reset('M')

            # Loop over signal samples and compute a combined signal histogram
            signal_histogram = None
            for signal in itervalues(signals):
                # Extract parameters
                process = signal['process']
                estimation = signal['estimation']

                # Compute the histogram
                result = estimation(distribution)(process, region)

                # Store or add it
                if signal_histogram is None:
                    signal_histogram = result
                else:
                    signal_histogram.Add(result)

            # Scale histogram if necessary and set title
            if signal_histogram is not None:
                if arguments.signal_scale != 1.0:
                    signal_histogram.Scale(arguments.signal_scale)
                    signal_histogram.SetTitle(
                        '{0} {1:.0f}x]'.format(
                            signal_histogram.GetTitle(),
                            arguments.signal_scale
                        )
                    )

            # Loop over background samples and compute their histograms
            background_histograms = []
            background_uncertainty_bands = []
            for background in itervalues(backgrounds):
                # Extract parameters
                process = background['process']
                estimation = background['estimation']
                uncertainties = background.get('uncertainties', [])

                # Compute the nominal histogram
                background_histograms.append(
                    estimation(distribution)(process, region)
                )

                # Set up error bands
                sample_uncertainty_bands = []

                # Compute statistical uncertainties
                sample_uncertainty_bands.append(
                    uncertainty_band(
                        process,
                        region,
                        distribution,
                        None,
                        estimation
                    )
                )

                # Compute systematic uncertainties
                for uncertainty in uncertainties:
                    sample_uncertainty_bands.append(
                        uncertainty_band(
                            process,
                            region,
                            distribution,
                            uncertainty,
                            estimation
                        )
                    )

                # Combine the uncertainties for this process
                if len(sample_uncertainty_bands) > 0:
                    background_uncertainty_bands.append(
                        combined_uncertainty_band(sample_uncertainty_bands)
                    )

            # Create a combined background histogram
            background_histogram = combined_histogram(background_histograms)

            # Compute combined uncertainties
            uncertainty = combined_uncertainty_band(
                background_uncertainty_bands,
                background_histogram,
                arguments.error_label
            )
            ratio_uncertainty = ratio_uncertainty_band(
                background_histogram,
                uncertainty
            )

            # If we're in capture mode, the histograms are bogus, so ignore
            # them
            if parallel.capturing():
                continue

            # Add text output if requested
            if arguments.text_counts:
                # Compute the text output path
                text_output_path = join(arguments.output,
                                        region_name,
                                        '{0}.txt'.format(distribution_name))

                # Save text
                with open(text_output_path, 'w') as f:
                    # Calculate s/sqrt(b)
                    s = signal_histogram.Integral(
                        1,
                        signal_histogram.GetNbinsX()
                    ) / arguments.signal_scale
                    b = background_histogram.Integral(
                        1,
                        background_histogram.GetNbinsX()
                    )
                    if b != 0.0:
                        f.write('s/sqrt(b): {0:.2f}\n\n'.format(s / sqrt(b)))
                    else:
                        f.write('b = 0.0, no s/sqrt(b)\n\n')

                    # Print out histogram content
                    for h in chain((data_histogram, signal_histogram),
                                   background_histograms):
                        f.write('--- {0} ---\n'.format(h.GetTitle()))
                        f.write('[{0} unweighted entries]\n'.format(
                            h.GetEntries()
                        ))
                        f.write('[{0} weighted entries]\n'.format(
                            h.Integral(1, h.GetNbinsX())
                        ))
                        for bin in range(1, h.GetNbinsX() + 1):
                            f.write(
                                '{0:.2f}-{1:.2f}: {2:.2f}+/-{3:.2f}\n'.format(
                                    h.GetBinLowEdge(bin),
                                    h.GetBinLowEdge(bin + 1),
                                    h.GetBinContent(bin),
                                    h.GetBinError(bin)
                                )
                            )
                        f.write('\n')

            # Set all histogram titles to include their counts, including those
            # which might be in underflow/overflow bins, unless told otherwise
            if not arguments.no_counts:
                for h in chain((data_histogram, signal_histogram),
                               background_histograms):
                    if h is not None:
                        h.SetTitle('{0} ({1:.1f})'.format(
                            h.GetTitle(),
                            h.Integral(1, h.GetNbinsX())
                        ))

            # Create a background stack
            background_stack = histogram_stack(*background_histograms)

            # Create a ratio plot
            ratio = ratio_histogram(data_histogram, background_stack)

            # TODO: Implement parallel plotting. Implement and use the
            # owls_taunu.taujets.plot_model() function.
            # Create a plot
            plot = Plot('',
                        distribution.x_label(),
                        distribution.y_label(),
                        ratio = True)

            # Draw the histograms
            plot.draw(((background_stack, uncertainty), None, 'hist'),
                      (signal_histogram, None, 'hist'),
                      (data_histogram, None, 'ep'))

            # Draw the ratio plot
            plot.draw_ratio_histogram(ratio, error_band = ratio_uncertainty)

            # Draw a legend
            # TODO: We want the data histogram on top of the legend, and
            # therefore we need to provide (drawable, style) to draw_legend.
            # Because of the way that ROOT TColor works with hex colours, we
            # can't simply style the histogram before plotting.
            # As a workaround, we could use the drawable title to identify
            # the drawable in the Plot object, but that's unreliable.
            #plot.draw_legend(data_histogram,
                             #signal_histogram,
                             #background_stack)
            plot.draw_legend()

            # Draw an ATLAS stamp
            plot.draw_atlas_label(luminosity,
                                  sqrt_s,
                                  custom_label = [region.label()],
                                  atlas_label = None)

            # Compute the plot output path
            plot_output_path = join(arguments.output,
                                    region_name,
                                    distribution_name)

            # Save plot
            plot.save(plot_output_path, arguments.extensions)
