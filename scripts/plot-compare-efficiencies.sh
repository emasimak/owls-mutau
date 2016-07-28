#!/bin/bash

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

EXTENSIONS="pdf"

# Plots with OS-SS backgrounds
LUMINOSITY=3193.68 # 1/pb
FILES="\
  results/plots_tau_efficiency/mc15b/mu_tau_medium_id/tau_efficiencies.root \
  results/plots_tau_efficiency/2015/mu_tau_medium_id/tau_efficiencies.root \
  "

OUTPUT="results/plots_tau_efficiency/compare/compare_20_1_20_7"
"$OWLS/tools/compare-efficiencies.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --files $FILES \
  --labels Data\ 2015\ \(20.1\) Data\ 2015\ \(20.7\) \
  --trigger tau25 \
  --label Data\ 2015 HLT_tau25_medium1_tracktwo \
  -- \
  luminosity=$LUMINOSITY


# Plots with OS-SS backgrounds
LUMINOSITY=7587.26 # 1/pb
FILES="\
  results/plots_tau_efficiency/2015/mu_tau_medium_id/tau_efficiencies.root \
  results/plots_tau_efficiency/2016/mu_tau_medium_id/tau_efficiencies.root \
  "
OUTPUT="results/plots_tau_efficiency/compare/compare_2015_2016"
"$OWLS/tools/compare-efficiencies.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --files $FILES \
  --labels Data\ 2015 Data\ 2016 \
  --trigger tau25 \
  --label Data\ 2015,\ 2016 HLT_tau25_medium1_tracktwo
