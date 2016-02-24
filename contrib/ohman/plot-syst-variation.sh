#!/usr/bin/env sh

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
REGIONS="\
  mu_tau_os mu_tau_tau25_os \
  mu_tau_ttbar_cr_os mu_tau_ttbar_cr_tau25_os \
  "

DISTRIBUTIONS="tau_pt"

${CONTRIB}/plot-syst-variation.py \
  --output results_mutau/systematics \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models-2016-01-21.py" \
  --regions-file "$OWLS/share/mutau/regions-2016-01-21.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  data_prefix="/disk/d1/ohman/tagprobe_2016-01-21_merged/"
