#!/bin/bash

# Compute the path to the owls-vh directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

# Configure masses
# MASSES=(350 400 1000 1400)
MASSES=(350)

# Execute plotting
for mass in ${MASSES[@]}; do
  # Plot OS-SS regions
  "$OWLS/tools/plot.py" \
    --output "results/plots_taujets/$mass" \
    --configuration "$OWLS/share/lephad/plot-configuration.py" \
    --model "mc" \
    --model-file "$OWLS/share/lephad/models.py" \
    --regions-file "$OWLS/share/lephad/regions.py" \
    --distributions-file "$OWLS/share/lephad/distributions.py" \
    --environment-file "$CONTRIB/environment.py" \
    --error-label "Stat. #oplus Sys. Unc." \
    higgs_mass=$mass \
    data_prefix=~/data/one/taujetsSFv00-00_merged/ \
    enable_systematics=False
done
