#!/usr/bin/env sh

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
REGIONS="\
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  "

DISTRIBUTIONS="tau_pt"

${CONTRIB}/plot-syst-variation.py \
  --output results_mutau/systematics \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models-2016-01-21.py" \
  --model osss_sub \
  --regions-file "$OWLS/share/mutau/regions-2016-01-21.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  data_prefix="/disk/d1/ohman/tagprobe_2016-01-21_merged/"


#${CONTRIB}/plot-syst-variation.py \
  #--output results_mutau/systematics_mc \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/mutau/models-2016-01-21.py" \
  #--model mc_sub \
  #--regions-file "$OWLS/share/mutau/regions-2016-01-21.py" \
  #--regions mu_tau_os \
  #--distributions-file "$OWLS/share/mutau/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--label "Bkg MC (OS)" \
  #data_prefix="/disk/d1/ohman/tagprobe_2016-01-21_merged/"
