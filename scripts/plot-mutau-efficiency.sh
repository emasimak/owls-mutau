#!/bin/bash

# Compute the path to the owls-taujets directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

EXTENSIONS="pdf"
EXTENSIONS="$EXTENSIONS eps"

TAU_PT=60

echo ">>> Plotting tau efficiency and scale factors for 2015 data"
LUMINOSITY=3193.68 # 1/pb
YEAR=2015
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"

REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight)
#REGIONS=(mu_tau_medium)


#OUTPUT="results/plots_tau_efficiency/$YEAR/tau25"
#declare -A triggers=(
  #["tau25"]="tau_pt_tau25"
  #["tau35"]="tau_pt_tau35"
  #["tau80"]="tau_pt_tau80"
  #)
#for REGION in ${REGIONS[@]}
#do
  #for trigger in ${!triggers[@]}
  #do
    #"$OWLS/tools/plot-tau-efficiency.py" \
      #--output "$OUTPUT/$REGION" \
      #--extensions $EXTENSIONS \
      #--model-file "$OWLS/definitions/models-v12.py" \
      #--model osss_sub \
      #--regions-file "$OWLS/definitions/regions-v12.py" \
      #--region $REGION \
      #--distributions-file "$OWLS/definitions/distributions.py" \
      #--distribution ${triggers[$trigger]} \
      #--triggers $trigger \
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
declare -A triggers=(
  ["tau25"]="tau_pt_trig_from60"
  ["tau35"]="tau_pt_trig_from60"
  ["tau80"]="tau_pt_tau80"
  )
for REGION in ${REGIONS[@]}
do
  for trigger in ${!triggers[@]}
  do
    "$OWLS/tools/plot-tau-efficiency.py" \
      --output "$OUTPUT/$REGION" \
      --extensions $EXTENSIONS \
      --model-file "$OWLS/definitions/models-v12.py" \
      --model osss_sub \
      --regions-file "$OWLS/definitions/regions-v12.py" \
      --region $REGION \
      --distributions-file "$OWLS/definitions/distributions.py" \
      --distribution ${triggers[$trigger]} \
      --triggers $trigger \
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

#REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight ttbar_cr 1bjet_cr)
REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight ttbar_cr)
#REGIONS=(mu_tau_loose mu_tau_medium mu_tau_tight)
#REGIONS=(mu_tau_medium)

#OUTPUT="results/plots_tau_efficiency/$YEAR/tau25"
#declare -A triggers=(
  #["tau25"]="tau_pt_tau25"
  #["tau35"]="tau_pt_tau35"
  #["tau50_L1TAU12"]="tau_pt_tau50"
  #["tau80"]="tau_pt_tau80"
  #["tau80_L1TAU60"]="tau_pt_tau80"
  #["tau125"]="tau_pt_tau125"
  #["tau160"]="tau_pt_tau160"
  #)
#for REGION in ${REGIONS[@]}
#do
  #for trigger in ${!triggers[@]}
  #do
    #"$OWLS/tools/plot-tau-efficiency.py" \
      #--output "$OUTPUT/$REGION" \
      #--extensions $EXTENSIONS \
      #--model-file "$OWLS/definitions/models-v12.py" \
      #--model osss_sub \
      #--regions-file "$OWLS/definitions/regions-v12.py" \
      #--region $REGION \
      #--distributions-file "$OWLS/definitions/distributions.py" \
      #--distribution ${triggers[$trigger]} \
      #--triggers $trigger \
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
declare -A triggers=(
  ["tau25"]="tau_pt_trig_from60"
  ["tau35"]="tau_pt_trig_from60"
  ["tau50_L1TAU12"]="tau_pt_trig_from60"
  ["tau80"]="tau_pt_tau80"
  ["tau80_L1TAU60"]="tau_pt_tau80"
  ["tau125"]="tau_pt_tau125"
  ["tau160"]="tau_pt_tau160"
  )
for REGION in ${REGIONS[@]}
do
  for trigger in ${!triggers[@]}
  do
    "$OWLS/tools/plot-tau-efficiency.py" \
      --output "$OUTPUT/$REGION" \
      --extensions $EXTENSIONS \
      --model-file "$OWLS/definitions/models-v12.py" \
      --model osss_sub \
      --regions-file "$OWLS/definitions/regions-v12.py" \
      --region $REGION \
      --distributions-file "$OWLS/definitions/distributions.py" \
      --distribution ${triggers[$trigger]} \
      --triggers $trigger \
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
