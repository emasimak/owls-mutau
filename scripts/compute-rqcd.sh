#!/bin/bash

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

REGIONS=""
REGIONS="\
  $REGIONS \
  qcd_cr \
  "
REGIONS="\
  $REGIONS \
  qcd_cr_1p \
  qcd_cr_3p \
  "
REGIONS="\
  $REGIONS \
  qcd_cr_tau25 \
  "
REGIONS="\
  $REGIONS \
  qcd_cr_tau25_1p \
  qcd_cr_tau25_3p \
  "
REGIONS="\
  $REGIONS \
  qcd_cr_very_loose \
  qcd_cr_very_loose_1p \
  qcd_cr_very_loose_3p \
  qcd_cr_loose \
  qcd_cr_loose_1p \
  qcd_cr_loose_3p \
  qcd_cr_medium \
  qcd_cr_medium_1p \
  qcd_cr_medium_3p \
  qcd_cr_tight \
  qcd_cr_tight_1p \
  qcd_cr_tight_3p \
  qcd_cr_very_loose_tau25 \
  qcd_cr_very_loose_tau25_1p \
  qcd_cr_very_loose_tau25_3p \
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

TAU_PT=60

# Compute r_QCD
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"
YEAR=2015
"$OWLS/tools/compute-rqcd.py" \
  --output results/rqcd/$YEAR/tau25 \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --environment-file "$SCRIPTS/environment.py" \
  data_prefix=$DATA_PREFIX \
  year=$YEAR

"$OWLS/tools/compute-rqcd.py" \
  --output results/rqcd/$YEAR/tau$TAU_PT \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --environment-file "$SCRIPTS/environment.py" \
  --high-pt \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT


DATA_PREFIX="/disk/d3/ohman/lhtnp_v19_merged"
YEAR=2016
"$OWLS/tools/compute-rqcd.py" \
  --output results/rqcd/$YEAR/tau25 \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --environment-file "$SCRIPTS/environment.py" \
  data_prefix=$DATA_PREFIX \
  year=$YEAR

"$OWLS/tools/compute-rqcd.py" \
  --output results/rqcd/$YEAR/tau$TAU_PT \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --environment-file "$SCRIPTS/environment.py" \
  --high-pt \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT
