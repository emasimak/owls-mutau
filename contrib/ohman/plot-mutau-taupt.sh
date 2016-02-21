#!/bin/bash


# Plot tau pT for a wide range of regions


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS=" \
  mu_tau_gradient_os \
  mu_tau_ttbar_cr_os \
  mu_tau_1b_cr_os \
  "
OSSS_REGIONS=" \
  mu_tau_gradient \
  mu_tau_gradient_1p \
  mu_tau_gradient_3p \
  mu_tau_ttbar_cr \
  mu_tau_ttbar_cr_1p \
  mu_tau_ttbar_cr_3p \
  mu_tau_1b_cr \
  mu_tau_1b_cr_1p \
  mu_tau_1b_cr_3p \
  "

DISTRIBUTIONS="tau_pt tau_pt_b2"
DISTRIBUTIONS=" \
  tau_pt \
  tau_pt_b2 \
  tau_eta \
  tau_phi \
  tau_bdt_score \
  mu_pt \
  mu_eta \
  mu_phi \
  jet_multiplicity \
  bjet_multiplicity \
  tau_n_tracks \
  tau_n_trk_core_wide \
  mt \
  "

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-21_merged/"



## Plots with only MC backgrounds, and split into MC processes
#OUTPUT="results_mutau/plots_mc"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/mutau/models.py" \
  #--model mc \
  #--regions-file "$OWLS/share/mutau/regions.py" \
  #--regions $MC_REGIONS \
  #--distributions-file "$OWLS/share/mutau/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY


## Plots with only MC backgrounds, and split into truth and fakes for ttbar
## and single top
#OUTPUT="results_mutau/plots_mc_fakes"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/mutau/models.py" \
  #--model mc_fakes \
  #--regions-file "$OWLS/share/mutau/regions.py" \
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
  --model-file "$OWLS/share/mutau/models.py" \
  --model osss_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
#DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-11_merged/"
#OUTPUT="results_mutau/plots_osss_fakes_2016-01-11"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/mutau/models_2016-01-11.py" \
  #--model osss_fakes \
  #--regions-file "$OWLS/share/mutau/regions.py" \
  #--regions $OSSS_REGIONS \
  #--distributions-file "$OWLS/share/mutau/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY
