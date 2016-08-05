#!/bin/bash


# Plot many distributions for
# - OS Data vs MC
# - OS-SS


# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  mu_tau_1p mu_tau_3p \
  mu_tau_tau25_os mu_tau_tau25_ss \
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "
MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  mu_tau_tau25_os mu_tau_tau25_ss \
  "

OSSS_REGIONS="\
  mu_tau \
  mu_tau_1p mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "
#OSSS_REGIONS="\
  #mu_tau60 \
  #mu_tau60_tau25 \
  #ttbar_cr_tau60 \
  #ttbar_cr_tau25_tau60 \
  #"
OSSS_REGIONS="\
  mu_tau \
  mu_tau_tau25 \
  ttbar_cr \
  ttbar_cr_tau25 \
  "

# All kinematic distributions
DISTRIBUTIONS="\
  tau_pt tau_eta tau_phi tau_n_tracks tau_bdt_score \
  mu_pt mu_eta mu_phi \
  mu_iso_var_trk_b2 mu_iso_topo_cal_b2 \
  bjet_multiplicity jet_multiplicity \
  met_et met_phi mt \
  deta dphi dr \
  "

EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"


LUMINOSITY=7587.26 # 1/pb
YEAR=2016

## Plots with MC backgrounds only
#OUTPUT="results/plots_mc/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model mc \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $MC_REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--label "MC15C, 20.7, Data $YEAR" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds
OUTPUT="results/plots_osss_fakes/$YEAR"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15C, 20.7, Data $YEAR" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY
