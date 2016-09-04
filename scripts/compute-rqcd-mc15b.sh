#!/bin/bash

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

REGIONS="\
  qcd_cr \
  qcd_cr_1p \
  qcd_cr_3p \
  qcd_cr_loose \
  qcd_cr_loose_1p \
  qcd_cr_loose_3p \
  qcd_cr_medium \
  qcd_cr_medium_1p \
  qcd_cr_medium_3p \
  qcd_cr_tight \
  qcd_cr_tight_1p \
  qcd_cr_tight_3p \
  qcd_cr_tau25 \
  qcd_cr_tau25_1p \
  qcd_cr_tau25_3p \
  qcd_cr_loose_tau25 \
  qcd_cr_loose_tau25_1p \
  qcd_cr_loose_tau25_3p \
  qcd_cr_medium_tau25 \
  qcd_cr_medium_tau25_1p \
  qcd_cr_medium_tau25_3p \
  qcd_cr_tight_tau25 \
  qcd_cr_tight_tau25_1p \
  qcd_cr_tight_tau25_3p \
  "
#REGIONS="qcd_cr"
#REGIONS="\
  #qcd_cr \
  #qcd_cr_1p \
  #qcd_cr_3p \
  #"

DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"

# Compute r_QCD
"$OWLS/tools/compute-rqcd.py" \
  --output results/rqcd/mc15b \
  --model-file "$OWLS/definitions/models-2016-01-21.py" \
  --model osss \
  --regions-file "$OWLS/definitions/regions-2016-01-21.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --environment-file "$SCRIPTS/environment.py" \
  data_prefix=$DATA_PREFIX
