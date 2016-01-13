#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

REGIONS="qcd_cr1 qcd_cr2 qcd_cr3 qcd_cr4 qcd_cr5"
DATA_PREFIX="/disk/d1/ohman/tagprobe_2015-11-09_merged"

# Compute r_QCD
"$OWLS/tools/compute-rqcd.py" \
  --model-file "$OWLS/share/mutau/models.py" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $REGIONS \
  --environment-file "$CONTRIB/environment.py" \
  --output "$OWLS/share/mutau/r_qcd.dict" \
  data_prefix=$DATA_PREFIX
