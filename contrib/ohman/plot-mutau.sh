#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

REGIONS="mu_tau mu_tau_1p mu_tau_3p mu_tau_tight mu_tau_os mu_tau_ss"
DISTRIBUTIONS="tau_pt tau_pt_alt tau_pt_alt2 tau_eta tau_phi \
  tau_bdt_score tau_n_tracks \
  mu_pt mu_eta mu_phi deta_mutau dphi_mutau \
  met_et met_phi dphi mt \
  mu nvx bjet_multiplicity jet_multiplicity"
#DISTRIBUTIONS="tau_pt"
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

# Plot with MC estimation, jet/e/mu fakes split
"$OWLS/tools/plot.py" \
  --output "results/plots_mutau" \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/taujets/models.py" \
  --model "mc_fakes2" \
  --regions-file "$OWLS/share/taujets/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/taujets/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY
