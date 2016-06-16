#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS=" \
  mu_tau_os \
  mu_tau_ss \
  mu_tau_1p_os \
  mu_tau_1p_ss \
  mu_tau_3p_os \
  mu_tau_3p_ss \
  mu_tau_qcd_cr_os \
  mu_tau_qcd_cr_ss \
  mu_tau_qcd_cr_1p_os \
  mu_tau_qcd_cr_1p_ss \
  mu_tau_qcd_cr_3p_os \
  mu_tau_qcd_cr_3p_ss \
  mu_tau_qcd_cr_tau25_os \
  mu_tau_qcd_cr_tau25_ss \
  mu_tau_qcd_cr_tau25_1p_os \
  mu_tau_qcd_cr_tau25_1p_ss \
  mu_tau_qcd_cr_tau25_3p_os \
  mu_tau_qcd_cr_tau25_3p_ss \
  "
#MC_REGIONS="mu_tau"

OSSS_REGIONS=" \
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_loose_id \
  mu_tau_loose_id_1p \
  mu_tau_loose_id_3p \
  mu_tau_medium_id \
  mu_tau_medium_id_1p \
  mu_tau_medium_id_3p \
  mu_tau_tight_id \
  mu_tau_tight_id_1p \
  mu_tau_tight_id_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  mu_tau_loose_id_tau25 \
  mu_tau_loose_id_tau25_1p \
  mu_tau_loose_id_tau25_3p \
  mu_tau_medium_id_tau25 \
  mu_tau_medium_id_tau25_1p \
  mu_tau_medium_id_tau25_3p \
  mu_tau_tight_id_tau25 \
  mu_tau_tight_id_tau25_1p \
  mu_tau_tight_id_tau25_3p \
  mu_tau_ttbar_cr \
  mu_tau_ttbar_cr_1p \
  mu_tau_ttbar_cr_3p \
  mu_tau_ttbar_cr_tau25 \
  mu_tau_ttbar_cr_tau25_1p \
  mu_tau_ttbar_cr_tau25_3p \
  "
#OSSS_REGIONS="mu_tau"
OSSS_REGIONS="mu_tau_tau25"

OSSS_REGIONS_SYST=" \
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  "
#OSSS_REGIONS_SYST="mu_tau"

DISTRIBUTIONS="tau_pt"

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-05-31_v03_merged/"



# Plots with only MC backgrounds, and split into MC processes
OUTPUT="results_mutau/plots_mc"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models-2016-05-31.py" \
  --model mc \
  --regions-file "$OWLS/share/mutau/regions-2016-05-31.py" \
  --regions $MC_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY


## Plots with only MC backgrounds, and split into truth and fakes for ttbar
## and single top
#OUTPUT="results_mutau/plots_mc_fakes"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/mutau/models-2016-05-31.py" \
  #--model mc_fakes \
  #--regions-file "$OWLS/share/mutau/regions-2016-05-31.py" \
  #--regions $MC_REGIONS\
  #--distributions-file "$OWLS/share/mutau/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
OUTPUT="results_mutau/plots_osss_fakes"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models-2016-05-31.py" \
  --model osss_fakes \
  --regions-file "$OWLS/share/mutau/regions-2016-05-31.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

## Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
## single top
#OUTPUT="results_mutau/plots_osss_fakes_syst"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/mutau/models-2016-05-31.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/share/mutau/regions-2016-05-31.py" \
  #--regions $OSSS_REGIONS_SYST \
  #--distributions-file "$OWLS/share/mutau/distributions.py" \
  #--distributions tau_pt \
  #--environment-file "$CONTRIB/environment.py" \
  #--text-count \
  #--error-label "Stat. #oplus Sys. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=True \
  #luminosity=$LUMINOSITY
