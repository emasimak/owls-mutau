#!/bin/bash

# Compute the path to the owls-taujets directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

EXTENSIONS="pdf"
EXTENSIONS="$EXTENSIONS eps"

#DISTRIBUTIONS=(tau_pt_trig_b1 tau_pt_trig_b3)
DISTRIBUTIONS=(tau_pt_trig_b3)

TAU_PT=60

echo ">>> Plotting tau efficiency and scale factors for 2015 data"
LUMINOSITY=3193.68 # 1/pb
YEAR=2015
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"
TRIGGERS="tau25 tau35 tau80"
#TRIGGERS="tau25"
REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight)
#REGIONS=(mu_tau_medium)


#OUTPUT="results/plots_tau_efficiency/$YEAR/tau25"
#for REGION in ${REGIONS[@]}
#do
  #for DISTRIBUTION in ${DISTRIBUTIONS[@]}
  #do
    #"$OWLS/tools/plot-tau-efficiency.py" \
      #--output "$OUTPUT/$REGION" \
      #--extensions $EXTENSIONS \
      #--model-file "$OWLS/definitions/models-v12.py" \
      #--model osss_sub \
      #--regions-file "$OWLS/definitions/regions-v12.py" \
      #--region $REGION \
      #--distributions-file "$OWLS/definitions/distributions.py" \
      #--distribution $DISTRIBUTION \
      #--triggers $TRIGGERS \
      #--environment-file "$SCRIPTS/environment.py" \
      #--root-output \
      #--text-output \
      #-- \
      #data_prefix=$DATA_PREFIX \
      #year=$YEAR \
      #luminosity=$LUMINOSITY \
      #enable_systematics=Efficiency
  #done
#done

OUTPUT="results/plots_tau_efficiency/$YEAR/tau$TAU_PT"
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
      -- \
      data_prefix=$DATA_PREFIX \
      year=$YEAR \
      luminosity=$LUMINOSITY \
      tau_pt=$TAU_PT \
      enable_systematics=Efficiency
  done
done

echo ">>> Plotting tau efficiency and scale factors for 2016 data"
LUMINOSITY=11473.88 # 1/pb
YEAR=2016
DATA_PREFIX="/disk/d3/ohman/lhtnp_v19_merged"
TRIGGERS="tau25 tau35 tau50_L1TAU12 tau80 tau80_L1TAU60 tau125 tau160"
#TRIGGERS="tau25"
#REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight ttbar_cr 1bjet_cr)
REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight)
#REGIONS=(mu_tau_medium)


#OUTPUT="results/plots_tau_efficiency/$YEAR/tau25"
#for REGION in ${REGIONS[@]}
#do
  #for DISTRIBUTION in ${DISTRIBUTIONS[@]}
  #do
    #"$OWLS/tools/plot-tau-efficiency.py" \
      #--output "$OUTPUT/$REGION" \
      #--extensions $EXTENSIONS \
      #--model-file "$OWLS/definitions/models-v12.py" \
      #--model osss_sub \
      #--regions-file "$OWLS/definitions/regions-v12.py" \
      #--region $REGION \
      #--distributions-file "$OWLS/definitions/distributions.py" \
      #--distribution $DISTRIBUTION \
      #--triggers $TRIGGERS \
      #--environment-file "$SCRIPTS/environment.py" \
      #--root-output \
      #--text-output \
      #-- \
      #data_prefix=$DATA_PREFIX \
      #year=$YEAR \
      #luminosity=$LUMINOSITY \
      #enable_systematics=Efficiency
  #done
#done

OUTPUT="results/plots_tau_efficiency/$YEAR/tau$TAU_PT"
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
      -- \
      data_prefix=$DATA_PREFIX \
      year=$YEAR \
      luminosity=$LUMINOSITY \
      tau_pt=$TAU_PT \
      enable_systematics=Efficiency
  done
done
