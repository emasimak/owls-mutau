#!/bin/bash

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="mu_tau_os mu_tau_ss mu_tau_tau25_os \
  mu_tau_qcd_cr_os mu_tau_qcd_cr_tau25_os \
  mu_tau_w_cr_os mu_tau_w_cr mu_tau_w_cr_tau25_os \
  mu_tau_fake_cr_os mu_tau_fake_cr2_os mu_tau_fake_cr_tau25_os \
  qcd_cr1 qcd_cr2 qcd_cr3 qcd_cr4"
OSSS_REGIONS="mu_tau mu_tau_tau25 mu_tau_tau35 \
  mu_tau_qcd_cr1 mu_tau_qcd_cr2 mu_tau_qcd_cr3"
#REGIONS="mu_tau"
DISTRIBUTIONS="tau_pt tau_eta tau_phi \
  tau_bdt_score tau_n_tracks tau_n_trk_core_wide \
  mu_pt mu_eta mu_phi deta dphi dr \
  met_et met_phi mt \
  mu nvx bjet_multiplicity jet_multiplicity"
#DISTRIBUTIONS="tau_pt tau_n_trk_core_wide"
#DISTRIBUTIONS="tau_pt"
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3340.00 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2015-11-09_merged"

# Plot with MC estimation, jet/e/mu fakes split
OUTPUT="results_mutau/plots_mc"
rm -rf $OUTPUT

# Split MC processes
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model mc \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $MC_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

OUTPUT="results_mutau/plots_mc_fakes"
rm -rf $OUTPUT

# Fakes split in ttbar and single top
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model mc_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $MC_REGIONS\
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plot with OSSS estimation
OUTPUT="results_mutau/plots_osss_fakes"
rm -rf $OUTPUT

# Fakes split in ttbar and single top
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model "osss_fakes" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY
