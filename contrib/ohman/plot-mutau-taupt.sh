#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  mu_tau_tau25_os \
  mu_tau_loose_os mu_tau_loose_ss \
  mu_tau_loose_tau25_os \
  mu_tau_qcd_cr_os mu_tau_qcd_cr_ss \
  mu_tau_gradient_os mu_tau_gradient_ss \
  mu_tau_gradient_tau25_os \
  mu_tau_gradient_qcd_cr_os mu_tau_gradient_qcd_cr_ss \
  "

OSSS_REGIONS="\
  mu_tau \
  mu_tau_tau25 \
  mu_tau_loose \
  mu_tau_loose_tau25 \
  mu_tau_gradient \
  mu_tau_gradient_tau25 \
  "

DISTRIBUTIONS="tau_pt tau_pt_b2"
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-11_merged"



# Plots with only MC backgrounds, and split into MC processes
OUTPUT="results_mutau/plots_mc"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model mc \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $MC_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY


# Plots with only MC backgrounds, and split into truth and fakes for ttbar
# and single top
OUTPUT="results_mutau/plots_mc_fakes"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model mc_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $MC_REGIONS\
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
OUTPUT="results_mutau/plots_osss_fakes"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model osss_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY
