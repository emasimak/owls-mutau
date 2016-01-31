#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  mu_tau_1p mu_tau_3p \
  mu_tau70_100_os mu_tau70_100_ss \
  mu_tau70_100_1p mu_tau70_100_3p \
  mu_tau60_80_os mu_tau60_80_ss \
  mu_tau60_80_1p mu_tau60_80_3p \
  mu_tau60_150_os mu_tau60_150_ss \
  mu_tau60_150_1p mu_tau60_150_3p \
  "

OSSS_REGIONS="\
  mu_tau70_100 \
  mu_tau70_100_1p mu_tau70_100_3p \
  mu_tau60_80 \
  mu_tau60_80_1p mu_tau60_80_3p \
  mu_tau60_150 \
  mu_tau60_150_tau25_1p mu_tau60_150_tau25_3p \
  mu_tau60_150_1p mu_tau60_150_3p \
  "

  #mu_tau70_100_tau25_1p mu_tau70_100_tau25_3p \
  #mu_tau60_80_tau25_1p mu_tau60_80_tau25_3p \

DISTRIBUTIONS="\
  tau_pt tau_eta tau_phi \
  tau_bdt_score tau_n_tracks \
  mu_pt mu_eta mu_phi \
  bjet_multiplicity jet_multiplicity \
  deta dphi dr \
  met_et met_phi mt \
  mu nvx \
  "
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
