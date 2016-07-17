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
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "
MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  "

OSSS_REGIONS="\
  mu_tau \
  mu_tau_1p mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "

OSSS_SYST_REGIONS="\
  mu_tau \
  mu_tau_1p mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "

DISTRIBUTIONS="\
  tau_pt tau_eta tau_phi \
  tau_bdt_score tau_bdt_score_trig tau_n_tracks \
  mu_pt mu_eta mu_phi \
  bjet_multiplicity jet_multiplicity \
  deta dphi dr \
  met_et met_phi mt \
  mu nvx \
  "
DISTRIBUTIONS="mu"

EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged"


# Plots with only MC backgrounds, and split into MC processes
OUTPUT="results/plots_mc/mc15b"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-2016-01-21.py" \
  --model mc \
  --regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  --regions $MC_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY


## Plots with only MC backgrounds, and split into truth and fakes for ttbar
## and single top
#OUTPUT="results/plots_mc_fakes/mc15b"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-2016-01-21.py" \
  #--model mc_fakes \
  #--regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  #--regions $MC_REGIONS\
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
OUTPUT="results/plots_osss_fakes2/mc15b"
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
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
## single top
#OUTPUT="results/plots_osss_fakes_syst/mc15b"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-2016-01-21.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  #--regions $OSSS_SYST_REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--error-label "Stat. #oplus Sys. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY
