#!/bin/bash


# Plot many distributions for
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
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #mu_tau_1p \
  #mu_tau_3p \
  #"
OSSS_REGIONS="\
  $OSSS_REGIONS \
  mu_tau_tau25 \
  "
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #mu_tau_tau25_1p \
  #mu_tau_tau25_3p \
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
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #1bjet_cr \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #1bjet_cr_1p \
  #1bjet_cr_3p \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #1bjet_cr_tau25 \
  #"
#OSSS_REGIONS="\
  #$OSSS_REGIONS \
  #1bjet_cr_tau25_1p \
  #1bjet_cr_tau25_3p \
  #"



# All kinematic distributions
DISTRIBUTIONS=""
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  tau_eta \
  tau_phi \
  "
#DISTRIBUTIONS="\
  #$DISTRIBUTIONS \
  #tau_bdt_score_trig \
  #"
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  tau_bdt_score \
  tau_n_tracks \
  tau_decay_mode \
  "
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  mu_pt \
  mu_eta \
  mu_phi \
  "
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  bjet_multiplicity \
  jet_multiplicity \
  "
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  deta \
  dphi \
  dr \
  "
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  met_et \
  met_phi \
  mt \
  "
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  mu \
  nvx \
  "
# Weight distributions
#DISTRIBUTIONS="\
  #$DISTRIBUTIONS \
  #NOMINAL_pileup_combined_weight \
  #lep_0_NOMINAL_MuEffSF_Reco_QualMedium \
  #lep_0_NOMINAL_MuEffSF_IsoGradient \
  #lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoIsoGradient \
  #lep_0_NOMINAL_MuEffSF_HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoIsoGradient \
  #tau_0_NOMINAL_effSF_VeryLooseLlhEleOLR_electron  \
  #tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM  \
  #tau_0_NOMINAL_TAU_EFF_RECO  \
  #tau_0_NOMINAL_TAU_EFF_SELECTION \
  #"
#DISTRIBUTIONS="\
  #$DISTRIBUTIONS \
  #jet_NOMINAL_global_effSF_JVT \
  #jet_NOMINAL_global_effSF_MVX \
  #jet_NOMINAL_global_ineffSF_MVX \
  #"

# Different tau pT distribution for high pT selection
DISTRIBUTIONS_HIPT="\
  $DISTRIBUTIONS \
  tau_pt_b2 \
  "
DISTRIBUTIONS="\
  $DISTRIBUTIONS \
  tau_pt \
  "

EXTENSIONS="pdf"
EXTENSIONS="$EXTENSIONS eps"

# pT cut for HIPT distributions
TAU_PT=60

###############################################################################
# 2015
LUMINOSITY=3193.68 # 1/pb
YEAR=2015
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"

# OSSS; SYSTEMATICS
OUTPUT="results/plots_osss_fakes_syst/$YEAR/tau25"
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
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS_HIPT \
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

# OSSS; SYSTEMATICS
OUTPUT="results/plots_osss_fakes_syst/$YEAR/tau25"
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
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS_HIPT \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --error-label "Stat. #oplus Syst. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  tau_pt=$TAU_PT \
  enable_systematics=True \
  luminosity=$LUMINOSITY

