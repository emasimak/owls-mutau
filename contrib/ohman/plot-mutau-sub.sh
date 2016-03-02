#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

OSSS_REGIONS=" \
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  "
  #mu_tau_ttbar_cr \
  #mu_tau_ttbar_cr_1p \
  #mu_tau_ttbar_cr_3p \
  #mu_tau_ttbar_cr_tau25 \
  #mu_tau_ttbar_cr_tau25_1p \
  #mu_tau_ttbar_cr_tau25_3p \
  #"
#OSSS_REGIONS="mu_tau"

DISTRIBUTIONS=" \
  tau_pt_trig \
  tau_pt_trig_b1 \
  tau_pt_trig_b2 \
  tau_pt_trig_b3 \
  "
#DISTRIBUTIONS="tau_pt_trig_b2"

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"


# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
OUTPUT="results_mutau/plots_osss_sub"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models-2016-01-21.py" \
  --model osss_sub \
  --regions-file "$OWLS/share/mutau/regions-2016-01-21.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY
