#!/bin/bash

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

REGIONS="\
  qcd_cr \
  qcd_cr_1p \
  qcd_cr_3p \
  qcd_cr_tau60 \
  qcd_cr_tau60_1p \
  qcd_cr_tau60_3p \
  qcd_cr_loose_id \
  qcd_cr_loose_id_1p \
  qcd_cr_loose_id_3p \
  qcd_cr_medium_id \
  qcd_cr_medium_id_1p \
  qcd_cr_medium_id_3p \
  qcd_cr_tight_id \
  qcd_cr_tight_id_1p \
  qcd_cr_tight_id_3p \
  qcd_cr_tau25 \
  qcd_cr_tau25_1p \
  qcd_cr_tau25_3p \
  qcd_cr_tau60_tau25 \
  qcd_cr_tau60_tau25_1p \
  qcd_cr_tau60_tau25_3p \
  qcd_cr_loose_id_tau25 \
  qcd_cr_loose_id_tau25_1p \
  qcd_cr_loose_id_tau25_3p \
  qcd_cr_medium_id_tau25 \
  qcd_cr_medium_id_tau25_1p \
  qcd_cr_medium_id_tau25_3p \
  qcd_cr_tight_id_tau25 \
  qcd_cr_tight_id_tau25_1p \
  qcd_cr_tight_id_tau25_3p \
  "
#REGIONS=" \
  #qcd_cr \
  #qcd_cr_1p \
  #qcd_cr_3p \
  #qcd_cr_tau25 \
  #qcd_cr_tau25_1p \
  #qcd_cr_tau25_3p \
  #"
#REGIONS="\
  #qcd_cr \
  #qcd_cr_1p \
  #qcd_cr_3p \
  #"

DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"

# Compute r_QCD
#YEAR=2015
#"$OWLS/tools/compute-rqcd.py" \
  #--output results/rqcd/$YEAR \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--environment-file "$SCRIPTS/environment.py" \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR

YEAR=2016
"$OWLS/tools/compute-rqcd.py" \
  --output results/rqcd/$YEAR \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --environment-file "$SCRIPTS/environment.py" \
  data_prefix=$DATA_PREFIX \
  year=$YEAR
