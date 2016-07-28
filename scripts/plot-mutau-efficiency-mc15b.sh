#!/bin/bash

# Compute the path to the owls-taujets directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

EXTENSIONS="pdf eps"
#EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"

TRIGGERS="tau25 tau35 tau80 tau125 tau160"
TRIGGERS="tau25"

REGIONS=(mu_tau_loose_id mu_tau_medium_id mu_tau_tight_id)
REGIONS=(mu_tau_medium_id)

#DISTRIBUTIONS=(tau_pt_trig_b1 tau_pt_trig_b3)
DISTRIBUTIONS=(tau_pt_trig_b3)

echo ">>> Plotting tau efficiency and scale factors"
OUTPUT="results/plots_tau_efficiency"

# tau efficiency
for REGION in ${REGIONS[@]}
do
  for DISTRIBUTION in ${DISTRIBUTIONS[@]}
  do
    OUTPUT="results/plots_tau_efficiency/mc15b/${REGION}"
    "$OWLS/tools/plot-tau-efficiency.py" \
      --output "$OUTPUT" \
      --extensions $EXTENSIONS \
      --model-file "$OWLS/definitions/models-2016-01-21.py" \
      --model osss_sub \
      --regions-file "$OWLS/definitions/regions-2016-01-21.py" \
      --region $REGION \
      --distributions-file "$OWLS/definitions/distributions.py" \
      --distribution $DISTRIBUTION \
      --triggers $TRIGGERS \
      --environment-file "$SCRIPTS/environment.py" \
      --root-output \
      --text-output \
      --label "MC15B, 20.1" \
      -- \
      data_prefix=$DATA_PREFIX \
      luminosity=$LUMINOSITY \
      enable_systematics=True
  done
done
