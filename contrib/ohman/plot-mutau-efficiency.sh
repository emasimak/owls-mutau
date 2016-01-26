#!/bin/bash

# Compute the path to the owls-taujets directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

EXTENSIONS="pdf eps"
#EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-11_merged"

echo ">>> Plotting tau efficiency and scale factors"
OUTPUT="results_mutau/plots_tau_efficiency"

# Tau efficiency
"$OWLS/tools/plot-tau-efficiency.py" \
  --output "$OUTPUT" \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model osss_sub \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --environment-file "$CONTRIB/environment.py" \
  --root-output \
  -- \
  data_prefix=$DATA_PREFIX
