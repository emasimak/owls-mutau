#!/usr/bin/env sh

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"

REGIONS=""
REGIONS="\
  $REGIONS \
  mu_tau \
  "
#REGIONS="\
  #$REGIONS \
  #mu_tau_1p \
  #mu_tau_3p \
  #"
REGIONS="\
  $REGIONS \
  mu_tau_tau25 \
  "
#REGIONS="\
  #$REGIONS \
  #mu_tau_tau25_1p \
  #mu_tau_tau25_3p \
  #"

DISTRIBUTIONS=""
DISTRIBUTIONS="\
  $DISTRIBUTIONS
  tau_pt
"

# Cut for high pT distributions
TAU_PT=60

SYSTEMATICS="Full"
SYSTEMATICS="Pruned"
#SYSTEMATICS="Efficiency"

LUMINOSITY=3193.68 # 1/pb
YEAR=2015
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"

OUTPUT="results/systematics/$YEAR/tau25"
"$OWLS/tools/plot-syst-variation.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  -- \
  data_prefix=$DATA_PREFIX \
  enable_systematics=$SYSTEMATICS \
  year=$YEAR

OUTPUT="results/systematics/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot-syst-variation.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  -- \
  data_prefix=$DATA_PREFIX \
  enable_systematics=$SYSTEMATICS \
  year=$YEAR \
  tau_pt=$TAU_PT

LUMINOSITY=11473.88 # 1/pb
YEAR=2016
DATA_PREFIX="/disk/d3/ohman/lhtnp_v19_merged"

OUTPUT="results/systematics/$YEAR/tau25"
"$OWLS/tools/plot-syst-variation.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  -- \
  data_prefix=$DATA_PREFIX \
  enable_systematics=$SYSTEMATICS \
  year=$YEAR

OUTPUT="results/systematics/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot-syst-variation.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  -- \
  data_prefix=$DATA_PREFIX \
  enable_systematics=$SYSTEMATICS \
  year=$YEAR \
  tau_pt=$TAU_PT
