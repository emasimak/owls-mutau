#!/bin/bash

# Compute the path to the owls-taujets directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

EXTENSIONS="pdf eps"
#EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-05-31_v03_merged/"

TRIGGERS="tau25 tau35 tau80 tau125 tau160"
#TRIGGERS="tau25 tau35"
TRIGGERS="tau25"

REGIONS=(mu_tau_loose_id mu_tau_medium_id mu_tau_tight_id)
#REGIONS=(mu_tau_medium_id)

DISTRIBUTIONS=(tau_pt_trig_b1 tau_pt_trig_b3)
DISTRIBUTIONS=(tau_pt_trig_b3)

echo ">>> Plotting tau efficiency and scale factors"
OUTPUT="results_mutau/plots_tau_efficiency"

# tau efficiency
for REGION in ${REGIONS[@]}
do
  for DISTRIBUTION in ${DISTRIBUTIONS[@]}
  do
    OUTPUT="results_mutau/plots_tau_efficiency/${REGION}_${DISTRIBUTION}"
    "$OWLS/tools/plot-tau-efficiency.py" \
      --output "$OUTPUT" \
      --extensions $EXTENSIONS \
      --model-file "$OWLS/share/mutau/models-2016-05-31.py" \
      --model osss_sub \
      --regions-file "$OWLS/share/mutau/regions-2016-05-31.py" \
      --region $REGION \
      --distributions-file "$OWLS/share/mutau/distributions.py" \
      --distribution $DISTRIBUTION \
      --triggers $TRIGGERS \
      --environment-file "$CONTRIB/environment.py" \
      --root-output \
      --text-output \
      -- \
      data_prefix=$DATA_PREFIX \
      enable_systematics=True
  done
done
