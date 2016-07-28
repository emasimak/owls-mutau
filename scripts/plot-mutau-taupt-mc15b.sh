#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

MC_REGIONS=" \
  mu_tau_os \
  mu_tau_ss \
  mu_tau_1p_os \
  mu_tau_1p_ss \
  mu_tau_3p_os \
  mu_tau_3p_ss \
  mu_tau_qcd_cr_os \
  mu_tau_qcd_cr_ss \
  mu_tau_qcd_cr_1p_os \
  mu_tau_qcd_cr_1p_ss \
  mu_tau_qcd_cr_3p_os \
  mu_tau_qcd_cr_3p_ss \
  mu_tau_qcd_cr_tau25_os \
  mu_tau_qcd_cr_tau25_ss \
  mu_tau_qcd_cr_tau25_1p_os \
  mu_tau_qcd_cr_tau25_1p_ss \
  mu_tau_qcd_cr_tau25_3p_os \
  mu_tau_qcd_cr_tau25_3p_ss \
  "
MC_REGIONS="\
  mu_tau_os \
  mu_tau_1p_os \
  mu_tau_3p_os \
  mu_tau_ss \
  mu_tau_1p_ss \
  mu_tau_3p_ss \
  "
#MC_REGIONS="mu_tau"

OSSS_REGIONS=" \
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_loose_id \
  mu_tau_loose_id_1p \
  mu_tau_loose_id_3p \
  mu_tau_medium_id \
  mu_tau_medium_id_1p \
  mu_tau_medium_id_3p \
  mu_tau_tight_id \
  mu_tau_tight_id_1p \
  mu_tau_tight_id_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  mu_tau_loose_id_tau25 \
  mu_tau_loose_id_tau25_1p \
  mu_tau_loose_id_tau25_3p \
  mu_tau_medium_id_tau25 \
  mu_tau_medium_id_tau25_1p \
  mu_tau_medium_id_tau25_3p \
  mu_tau_tight_id_tau25 \
  mu_tau_tight_id_tau25_1p \
  mu_tau_tight_id_tau25_3p \
  mu_tau_ttbar_cr \
  mu_tau_ttbar_cr_1p \
  mu_tau_ttbar_cr_3p \
  mu_tau_ttbar_cr_tau25 \
  mu_tau_ttbar_cr_tau25_1p \
  mu_tau_ttbar_cr_tau25_3p \
  "
OSSS_REGIONS=" \
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  "
#OSSS_REGIONS="\
  #mu_tau \
  #mu_tau_tau25 \
  #"
#OSSS_REGIONS="mu_tau"

DISTRIBUTIONS="\
  tau_pt \
  tau_pt_b2 \
  tau_pt_b3 \
  tau_pt_trig_b3 \
  "
#DISTRIBUTIONS="tau_pt"
#DISTRIBUTIONS="tau_pt_trig_b3"

EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"


## Plots with only MC backgrounds, and split into MC processes
#OUTPUT="results/plots_mc/mc15b"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-2016-01-21.py" \
  #--model mc \
  #--regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  #--regions $MC_REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--label "MC15B, 20.1" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# Plots with only MC backgrounds, and split into MC processes
OUTPUT="results/plots_mc_fakes/mc15b"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-2016-01-21.py" \
  --model mc_fakes \
  --regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  --regions $MC_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15B, 20.1" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds
OUTPUT="results/plots_osss_fakes/mc15b"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-2016-01-21.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15B, 20.1" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY
