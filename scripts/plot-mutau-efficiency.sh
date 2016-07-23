#!/bin/bash

# Compute the path to the owls-taujets directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

EXTENSIONS="pdf eps"
#EXTENSIONS="pdf"

TRIGGERS="tau25 tau35 tau80 tau125 tau160"
#TRIGGERS="tau25 tau35"
TRIGGERS="tau25 tau125"

REGIONS=(mu_tau_loose_id mu_tau_medium_id mu_tau_tight_id mu_tau_ttbar_cr)
#REGIONS=(mu_tau_medium_id)

#DISTRIBUTIONS=(tau_pt_trig_b1 tau_pt_trig_b3)
DISTRIBUTIONS=(tau_pt_trig_b3)

echo ">>> Plotting tau efficiency and scale factors for 2015 data"
LUMINOSITY=3193.68 # 1/pb
DATA_PREFIX="/disk/d2/ohman/lhtnp_v15_merged"
YEAR=2015
OUTPUT="results/plots_tau_efficiency/$YEAR"
for REGION in ${REGIONS[@]}
do
  for DISTRIBUTION in ${DISTRIBUTIONS[@]}
  do
    "$OWLS/tools/plot-tau-efficiency.py" \
      --output "$OUTPUT/$REGION" \
      --extensions $EXTENSIONS \
      --model-file "$OWLS/definitions/models-v12.py" \
      --model osss_sub \
      --regions-file "$OWLS/definitions/regions-v12.py" \
      --region $REGION \
      --distributions-file "$OWLS/definitions/distributions.py" \
      --distribution $DISTRIBUTION \
      --triggers $TRIGGERS \
      --environment-file "$SCRIPTS/environment.py" \
      --root-output \
      --text-output \
      --label "MC15C, 20.7" \
      -- \
      data_prefix=$DATA_PREFIX \
      year=$YEAR \
      luminosity=$LUMINOSITY \
      enable_systematics=True
  done
done

echo ">>> Plotting tau efficiency and scale factors for 2016 data"
LUMINOSITY=7980.0 # 1/pb
DATA_PREFIX="/disk/d2/ohman/lhtnp_v15_merged"
YEAR=2016
OUTPUT="results/plots_tau_efficiency/$YEAR"
for REGION in ${REGIONS[@]}
do
  for DISTRIBUTION in ${DISTRIBUTIONS[@]}
  do
    "$OWLS/tools/plot-tau-efficiency.py" \
      --output "$OUTPUT/$REGION" \
      --extensions $EXTENSIONS \
      --model-file "$OWLS/definitions/models-v12.py" \
      --model osss_sub \
      --regions-file "$OWLS/definitions/regions-v12.py" \
      --region $REGION \
      --distributions-file "$OWLS/definitions/distributions.py" \
      --distribution $DISTRIBUTION \
      --triggers $TRIGGERS \
      --environment-file "$SCRIPTS/environment.py" \
      --root-output \
      --text-output \
      --label "MC15C, 20.7" \
      -- \
      data_prefix=$DATA_PREFIX \
      year=$YEAR \
      luminosity=$LUMINOSITY \
      enable_systematics=True
  done
done
