#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

REGIONS="mu_tau mu_tau_1p mu_tau_3p mu_tau_tau25 mu_tau_tau35"
REGIONS="mu_tau mu_tau_tau25 mu_tau_tau35"
#REGIONS="mu_tau"
DISTRIBUTIONS="tau_pt tau_pt_alt tau_pt_alt2 tau_eta tau_phi \
  tau_bdt_score tau_n_tracks \
  mu_pt mu_eta mu_phi deta_mutau dphi_mutau \
  met_et met_phi dphi mt \
  mu nvx bjet_multiplicity jet_multiplicity"
DISTRIBUTIONS="tau_pt"
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=1011.48 # 1/pb
DATA_PREFIX=/disk/d0/ohman/taujetsSFv03-05_merged/

# NOTE: Keep for the future.
## Plot with MC estimation, no fake split
#"$OWLS/tools/plot.py" \
  #--output "results/plots_mutau_nofakes" \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/taujets/models.py" \
  #--model "mc" \
  #--regions-file "$OWLS/share/taujets/regions.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/share/taujets/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# NOTE: Keep for the future.
## Plot with MC estimation, jet/lepton fakes split
#"$OWLS/tools/plot.py" \
  #--output "results/plots_mutau_lfakes" \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/taujets/models.py" \
  #--model "mc_fakes" \
  #--regions-file "$OWLS/share/taujets/regions.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/share/taujets/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

#"$OWLS/tools/plot.py" \
  #--output "results/plots_mutau" \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/taujets/models.py" \
  #--model "mc_fakes2" \
  #--regions-file "$OWLS/share/taujets/regions.py" \
  #--regions mu_tau \
  #--distributions-file "$OWLS/share/taujets/distributions.py" \
  #--distributions tau_pt \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# Plot with MC estimation, jet/e/mu fakes split
OUTPUT="results/plots_mutau"
rm -rf $OUTPUT
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/taujets/models.py" \
  #--model "mc_fakes2" \
  #--regions-file "$OWLS/share/taujets/regions.py" \
  #--regions $REGIONS mu_tau_os mu_tau_ss \
  #--distributions-file "$OWLS/share/taujets/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/taujets/models.py" \
  --model "mc_fakes" \
  --regions-file "$OWLS/share/taujets/regions.py" \
  --regions mu_tau_jetfake \
  --distributions-file "$OWLS/share/taujets/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

## Plot with OSSS estimation, jet/e/mu fakes split
OUTPUT="results/plots_mutau_osss"
rm -rf $OUTPUT
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/taujets/models.py" \
  #--model "osss_fakes2" \
  #--regions-file "$OWLS/share/taujets/regions.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/share/taujets/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/taujets/models.py" \
  --model "osss_fakes" \
  --regions-file "$OWLS/share/taujets/regions.py" \
  --regions mu_tau_jetfake \
  --distributions-file "$OWLS/share/taujets/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plot with FF estimation, e/mu fakes split
#OUTPUT="results/plots_mutau_fakes"
#rm -rf $OUTPUT
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/share/taujets/models.py" \
  #--model "ff" \
  #--regions-file "$OWLS/share/taujets/regions.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/share/taujets/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$CONTRIB/environment.py" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY
