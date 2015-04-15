#!/bin/bash

# Compute the path to the owls-vh directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

"$OWLS/tools/plot-turnon.py" \
  --output "results/plots_trigger_sf" \
  --model-file "$OWLS/share/taujets/models_trigger_sf.py" \
  --regions-file "$OWLS/share/taujets/regions.py" \
  --distributions-file "$OWLS/share/taujets/distributions.py" \
  --environment-file "$CONTRIB/environment.py" \
  data_prefix=~/data/one/taujetsSFv00-01_merged/
