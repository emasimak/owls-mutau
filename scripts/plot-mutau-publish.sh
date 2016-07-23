#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

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

OSSS_REGIONS_SYST=" \
  mu_tau \
  mu_tau_tau25 \
  "
#OSSS_REGIONS_SYST="mu_tau"

DISTRIBUTIONS=" \
  tau_pt \
  tau_bdt_score_trig \
"

EXTENSIONS="pdf eps"
EXTENSIONS="pdf"

LUMINOSITY=3193.68 # 1/pb
DATA_PREFIX="/disk/d2/ohman/lhtnp_v15_merged"
YEAR=2015


# Plots with OS-SS backgrounds
OUTPUT="results/plots_publish/$YEAR"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15C, 20.7" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds with systematic uncertainties
#OUTPUT="results/plots_publish_syst/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/models-v12.py" \
  #--regions $OSSS_REGIONS_SYST \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--label "MC15C, 20.7" \
  #--error-label "Stat. #oplus Sys. Unc." \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY

LUMINOSITY=7980.0 # 1/pb
DATA_PREFIX="/disk/d2/ohman/lhtnp_v15_merged"
YEAR=2016

# Plots with OS-SS backgrounds
OUTPUT="results/plots_publish/$YEAR"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15C, 20.7" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds with systematic uncertainties
#OUTPUT="results/plots_publish_syst/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/models-v12.py" \
  #--regions $OSSS_REGIONS_SYST \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--label "MC15C, 20.7" \
  #--error-label "Stat. #oplus Sys. Unc." \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY
