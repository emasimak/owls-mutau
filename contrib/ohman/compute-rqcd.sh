#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

REGIONS="mu_tau mu_tau_jetfake"
DATA_PREFIX=/disk/d0/ohman/taujetsSFv03-05_merged/

# Compute r_QCD
"$OWLS/tools/compute-rqcd.py" \
  --model-file "$OWLS/share/taujets/models.py" \
  --regions-file "$OWLS/share/taujets/regions.py" \
  --regions $REGIONS \
  --environment-file "$CONTRIB/environment.py" \
  --output "$OWLS/share/taujets/r_qcd.dict" \
  data_prefix=$DATA_PREFIX
