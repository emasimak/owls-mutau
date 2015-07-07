#!/bin/bash

# Compute the path to the owls-vh directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."
OUTPUT="results/plots_trigmatch"

rm -rf "$OUTPUT"

"$OWLS/tools/plot-trigmatch.py" \
  --output "$OUTPUT" \
  --model-file "$OWLS/share/taujets/models_trigger_sf.py" \
  --regions-file "$OWLS/share/taujets/regions.py" \
  --distributions-file "$OWLS/share/taujets/distributions.py" \
  --environment-file "$CONTRIB/environment.py" \
  data_prefix=~/data/one/taujetsSFv02-06_merged/
