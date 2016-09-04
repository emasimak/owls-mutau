#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

REGIONS="\
  mu_tau_publish \
  mu_tau_publish_tau25 \
  "
#REGIONS="mu_tau_publish_tau25"

EXTENSIONS="pdf eps"
EXTENSIONS="pdf"

LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"

## Plots with OS-SS backgrounds
#OUTPUT="results/plots_publish/mc15b"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-2016-01-21.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds with systematic uncertainties
#OUTPUT="results/plots_publish_syst/mc15b"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/models-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. #oplus Sys. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY


LUMINOSITY=3193.68 # 1/pb
YEAR=2015
DATA_PREFIX="/disk/d3/ohman/lhtnp_v16_merged"

## Plots with OS-SS backgrounds
#OUTPUT="results/plots_publish/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions tau_pt \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. Unc." \
  #--no-counts \
  #--publish \
  #--ratio-title "Data / exp." \
  #-- \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

#OUTPUT="results/plots_publish/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions mu_tau_publish_tau25 \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions tau_bdt_score_trig \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. Unc." \
  #--no-counts \
  #--publish \
  #--ratio-title "Data / exp." \
  #-- \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds
#OUTPUT="results/plots_publish_syst/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions tau_pt \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. #oplus Sys. Unc." \
  #--no-counts \
  #--publish \
  #--ratio-title "Data / exp." \
  #-- \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY

#OUTPUT="results/plots_publish_syst/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions mu_tau_publish_tau25 \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions tau_bdt_score_trig \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. #oplus Sys. Unc." \
  #--no-counts \
  #--publish \
  #--ratio-title "Data / exp." \
  #-- \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY

OUTPUT="results/plots_publish_tau_efficiency/$YEAR"
REGION="mu_tau_publish"
DISTRIBUTION="tau_pt_trig_b3"
"$OWLS/tools/plot-tau-efficiency.py" \
  --output "$OUTPUT/$REGION" \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --region $REGION \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distribution $DISTRIBUTION \
  --triggers tau25 \
  --no-prong-separated \
  --publish \
  --environment-file "$SCRIPTS/environment.py" \
  -- \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  luminosity=$LUMINOSITY \
  enable_systematics=True

LUMINOSITY=7980.0 # 1/pb
DATA_PREFIX="/disk/d3/ohman/lhtnp_v19_merged"
YEAR=2016

## Plots with OS-SS backgrounds
#OUTPUT="results/plots_publish/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds with systematic uncertainties
#OUTPUT="results/plots_publish_syst/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/definitions/models-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--error-label "Stat. #oplus Sys. Unc." \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY
