#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="\
  mu_tau_os \
  mu_tau_ss \
  mu_tau_qcd_cr_os \
  mu_tau_qcd_cr_ss \
  mu_tau_w_cr_os \
  mu_tau_w_cr_ss \
  mu_tau_fake_cr_os \
  mu_tau_fake_cr_ss \
  mu_tau_fake_cr_bveto_os \
  mu_tau_fake_cr_bveto_ss \
  qcd_cr1 \
  qcd_cr2 \
  qcd_cr3 \
  qcd_cr4 \
  qcd_cr5"
OSSS_REGIONS="\
  mu_tau_rqcd1 \
  mu_tau_rqcd2 \
  mu_tau_rqcd3 \
  mu_tau_rqcd4 \
  mu_tau_rqcd5"
DISTRIBUTIONS="tau_pt"
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3340.00 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2015-11-09_merged"

# Plot with MC estimation, jet/e/mu fakes split
OUTPUT="results_mutau/plots_mc"

# Plots with only MC backgrounds, and split into MC processes
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

OUTPUT="results_mutau/plots_mc_fakes"

# Plots with only MC backgrounds, and split into truth and fakes for ttbar
# and single top
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

## Plot with OSSS estimation
OUTPUT="results_mutau/plots_osss_fakes"

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
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
