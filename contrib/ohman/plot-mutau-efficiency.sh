#!/bin/bash

# Compute the path to the owls-taujets directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"

echo ">>> Plotting tau efficiency and scale factors"
OUTPUT="results_mutau/plots_tau_efficiency"

# tau efficiency
for REGION in mu_tau
#for REGION in mu_tau mu_tau_ttbar_cr
do
  OUTPUT="results_mutau/plots_tau_efficiency/$REGION"
  "$OWLS/tools/plot-tau-efficiency.py" \
    --output "$OUTPUT" \
    --extensions $EXTENSIONS \
    --model-file "$OWLS/share/mutau/models-2016-01-21.py" \
    --model osss_sub \
    --regions-file "$OWLS/share/mutau/regions-2016-01-21.py" \
    --region $REGION \
    --distributions-file "$OWLS/share/mutau/distributions.py" \
    --environment-file "$CONTRIB/environment.py" \
    --root-output \
    --text-output \
    -- \
    data_prefix=$DATA_PREFIX \
    enable_systematics=True
done
