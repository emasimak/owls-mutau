#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

REGIONS="\
  mu_tau_qcd_cr \
  mu_tau_qcd_cr_1p \
  mu_tau_qcd_cr_3p \
  mu_tau_qcd_cr_loose_id \
  mu_tau_qcd_cr_loose_id_1p \
  mu_tau_qcd_cr_loose_id_3p \
  mu_tau_qcd_cr_medium_id \
  mu_tau_qcd_cr_medium_id_1p \
  mu_tau_qcd_cr_medium_id_3p \
  mu_tau_qcd_cr_tight_id \
  mu_tau_qcd_cr_tight_id_1p \
  mu_tau_qcd_cr_tight_id_3p \
  mu_tau_qcd_cr_tau25 \
  mu_tau_qcd_cr_tau25_1p \
  mu_tau_qcd_cr_tau25_3p \
  mu_tau_qcd_cr_loose_id_tau25 \
  mu_tau_qcd_cr_loose_id_tau25_1p \
  mu_tau_qcd_cr_loose_id_tau25_3p \
  mu_tau_qcd_cr_medium_id_tau25 \
  mu_tau_qcd_cr_medium_id_tau25_1p \
  mu_tau_qcd_cr_medium_id_tau25_3p \
  mu_tau_qcd_cr_tight_id_tau25 \
  mu_tau_qcd_cr_tight_id_tau25_1p \
  mu_tau_qcd_cr_tight_id_tau25_3p \
  "
#REGIONS="mu_tau_qcd_cr"

DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged"

# Compute r_QCD
"$OWLS/tools/compute-rqcd.py" \
  --output results_mutau/rqcd \
  --model-file "$OWLS/share/mutau/models-2016-01-21.py" \
  --model osss \
  --regions-file "$OWLS/share/mutau/regions-2016-01-21.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --environment-file "$CONTRIB/environment.py" \
  data_prefix=$DATA_PREFIX
