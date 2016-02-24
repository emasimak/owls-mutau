#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

REGIONS="\
  mu_tau_qcd_cr \
  mu_tau_qcd_cr_1p \
  mu_tau_qcd_cr_3p \
  "
  #mu_tau_qcd_cr_tau25 \
  #mu_tau_qcd_cr_tau25_1p \
  #mu_tau_qcd_cr_tau25_3p \
#REGIONS="mu_tau_qcd_cr"

DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged"

# Compute r_QCD
"$OWLS/tools/compute-rqcd.py" \
  --output results_mutau/rqcd \
  --model-file "$OWLS/share/mutau/models.py" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $REGIONS \
  --environment-file "$CONTRIB/environment.py" \
  data_prefix=$DATA_PREFIX
