#!/usr/bin/env sh

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

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
REGIONS="\
  mu_tau \
  mu_tau_tau25 \
  "

DISTRIBUTIONS="tau_pt"

"$OWLS/tools/plot-syst-variation.py" \
  --output results/systematics/mc15b \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-2016-01-21.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  -- \
  enable_systematics=Pruned \
  data_prefix="/disk/d1/ohman/tagprobe_2016-01-21_merged/"
