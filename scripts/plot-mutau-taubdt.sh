#!/bin/bash


# Plot tau pT for a wide range of regions
# - MC with fakes
# - OS-SS
# - OS-SS with systematic uncertainties
# - tau pT > 25 GeV
# - tau pT > 60 GeV
# - 2015 data
# - 2016 data


# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

OSSS_REGIONS=""
OSSS_REGIONS="\
  $OSSS_REGIONS \
  mu_tau \
  "
OSSS_REGIONS="\
  $OSSS_REGIONS \
  mu_tau_1p \
  mu_tau_3p \
  "
OSSS_REGIONS="\
  $OSSS_REGIONS \
  mu_tau_tau25 \
  "
OSSS_REGIONS="\
  $OSSS_REGIONS \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  "
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #mu_tau_loose \
  #mu_tau_loose_1p \
  #mu_tau_loose_3p \
  #mu_tau_medium \
  #mu_tau_medium_1p \
  #mu_tau_medium_3p \
  #mu_tau_tight \
  #mu_tau_tight_1p \
  #mu_tau_tight_3p \
  #mu_tau_loose_tau25 \
  #mu_tau_loose_tau25_1p \
  #mu_tau_loose_tau25_3p \
  #mu_tau_medium_tau25 \
  #mu_tau_medium_tau25_1p \
  #mu_tau_medium_tau25_3p \
  #mu_tau_tight_tau25 \
  #mu_tau_tight_tau25_1p \
  #mu_tau_tight_tau25_3p \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #ttbar_cr \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #ttbar_cr_1p \
  #ttbar_cr_3p \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #ttbar_cr_tau25 \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #ttbar_cr_tau25_1p \
  #ttbar_cr_tau25_3p \
  #"
OSSS_SYST_REGIONS=$OSSS_REGIONS


DISTRIBUTIONS=""
DISTRIBUTIONS="\
  $DISTRIBUTIONS
  tau_bdt_score
"

EXTENSIONS="pdf"
EXTENSIONS="$EXTENSIONS eps"

# Cut for high pT distributions
TAU_PT=60


###############################################################################
# 2015
LUMINOSITY=3193.68 # 1/pb
YEAR=2015
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"

# OSSS
OUTPUT="results/plots_osss_fakes/$YEAR/tau25"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY
OUTPUT="results/plots_osss_fakes/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# OSSS; SYSTEMATICS
OUTPUT="results/plots_osss_fakes_syst/$YEAR/tau25"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_SYST_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. #oplus Syst. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=True \
  luminosity=$LUMINOSITY
OUTPUT="results/plots_osss_fakes_syst/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_SYST_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. #oplus Syst. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=True \
  luminosity=$LUMINOSITY


###############################################################################
# 2016
LUMINOSITY=11473.88 # 1/pb
YEAR=2016
DATA_PREFIX="/disk/d3/ohman/lhtnp_v19_merged"

# OSSS
OUTPUT="results/plots_osss_fakes/$YEAR/tau25"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY
OUTPUT="results/plots_osss_fakes/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# OSSS; SYSTEMATICS
OUTPUT="results/plots_osss_fakes_syst/$YEAR/tau25"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_SYST_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. #oplus Syst. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=True \
  luminosity=$LUMINOSITY
OUTPUT="results/plots_osss_fakes_syst/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_SYST_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. #oplus Syst. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=True \
  luminosity=$LUMINOSITY
