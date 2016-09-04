#!/bin/bash


# Plot many distributions for
# - OS Data vs MC
# - OS-SS


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
  mu_tau_tau25 \
  "
OSSS_REGIONS="\
  $OSSS_REGIONS \
  ttbar_cr \
  "
OSSS_REGIONS="\
  $OSSS_REGIONS \
  ttbar_cr_tau25 \
  "
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #1bjet_cr \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #1bjet_cr_tau25 \
  #"

OSSS_REGIONS_1p=""
OSSS_REGIONS_1p="\
  $OSSS_REGIONS_1p \
  mu_tau_1p \
  "
OSSS_REGIONS_1p="\
  $OSSS_REGIONS_1p \
  mu_tau_tau25_1p \
  "
OSSS_REGIONS_1p="\
  $OSSS_REGIONS_1p \
  mu_tau_very_loose_1p \
  "
OSSS_REGIONS_1p="\
  $OSSS_REGIONS_1p \
  mu_tau_very_loose_tau25_1p \
  "
#OSSS_REGIONS_1p="\
  #$OSSS_REGIONS_1p \
  #ttbar_cr_1p \
  #"
#OSSS_REGIONS_1p="\
  #$OSSS_REGIONS_1p \
  #ttbar_cr_tau25_1p \
  #"
#OSSS_REGIONS_1p="\
  #$OSSS_REGIONS_1p \
  #1bjet_cr_1p \
  #"
#OSSS_REGIONS_1p="\
  #$OSSS_REGIONS_1p \
  #1bjet_cr_tau25_1p \
  #"

#OSSS_REGIONS_3p=""
#OSSS_REGIONS_3p="\
  #$OSSS_REGIONS_3p \
  #mu_tau_3p \
  #"
#OSSS_REGIONS_3p="\
  #$OSSS_REGIONS_3p \
  #mu_tau_tau25_3p \
  #"
#OSSS_REGIONS_3p="\
  #$OSSS_REGIONS_3p \
  #ttbar_cr_3p \
  #"
#OSSS_REGIONS_3p="\
  #$OSSS_REGIONS_3p \
  #ttbar_cr_tau25_3p \
  #"
#OSSS_REGIONS_3p="\
  #$OSSS_REGIONS_3p \
  #1bjet_cr_3p \
  #"
#OSSS_REGIONS_3p="\
  #$OSSS_REGIONS_3p \
  #1bjet_cr_tau25_3p \
  #"


# All kinematic distributions
DISTRIBUTIONS=""
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  tau_decay_mode \
  "

# All kinematic distributions
DISTRIBUTIONS_1p=""
DISTRIBUTIONS_1p="\
  $DISTRIBUTIONS_1p \
  tau_ip_sig_ld_trk \
  tau_ip_sig_ld_trk_corr \
  tau_trig_ip_sig_ld_trk \
  tau_trig_ip_sig_ld_trk_corr \
  "


EXTENSIONS="pdf eps"
EXTENSIONS="pdf"

TAU_PT=60

###############################################################################
# 2016
LUMINOSITY=11473.88 # 1/pb
YEAR=2016
DATA_PREFIX="/disk/d3/ohman/lhtnp_v19_merged"

OUTPUT="results/plots_osss_fakes_extra/$YEAR/tau$TAU_PT"
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

OUTPUT="results/plots_osss_fakes_extra/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS_1p \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS_1p \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=False \
  luminosity=$LUMINOSITY

OUTPUT="results/plots_osss_fakes_extra/$YEAR/tau$TAU_PT"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS_1p \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS_3p \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=False \
  luminosity=$LUMINOSITY
