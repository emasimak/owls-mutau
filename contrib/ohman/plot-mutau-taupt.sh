#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="\
  mu_tau_os \
  mu_tau_tau25_os \
  mu_tau_ss \
  mu_tau_4_8_os \
  mu_tau_4_8_ss \
  mu_tau_6_10_os \
  mu_tau_6_10_ss \
  mu_tau_10_13_os \
  mu_tau_10_13_tau25_os \
  mu_tau_10_13_ss \
  mu_tau_qcd_cr \
  mu_tau_qcd_cr_os \
  mu_tau_qcd_cr_ss \
  mu_tau_w_cr \
  mu_tau_w_cr_os \
  mu_tau_w_cr_ss \
  mu_tau_w_cr2 \
  mu_tau_w_cr2_os \
  mu_tau_w_cr2_ss \
  mu_tau_w_cr3 \
  mu_tau_w_cr3_os \
  mu_tau_w_cr3_ss \
  "

OSSS_REGIONS="\
  mu_tau \
  mu_tau_tau25 \
  mu_tau_btag_rqcd \
  mu_tau_4_8 \
  mu_tau_6_10 \
  mu_tau_10_13 \
  mu_tau_10_13_tau25 \
  mu_tau_w_cr \
  "

DISTRIBUTIONS="tau_pt tau_pt_b2 mt"
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3340.00 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2015-11-09_merged"


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
