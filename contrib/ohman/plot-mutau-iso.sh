#!/bin/bash


# Plot muon track and calo isolation variables for different regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="\
  mu_tau_noiso \
  mu_tau \
  mu_tau_loose \
  mu_tau_qcd_cr \
  mu_tau_gradient \
  mu_tau_gradient_qcd_cr
"
DISTRIBUTIONS="\
  mu_iso_trk \
  mu_iso_cal \
  mu_iso_var_trk \
  mu_iso_topo_cal \
"
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-11_merged"


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
