#!/usr/bin/env sh

# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
REGIONS="\
  mu_tau_os mu_tau_tau25_os \
  mu_tau_ttbar_cr_os mu_tau_ttbar_cr_tau25_os \
  mu_tau_1b_cr_os \
  "
DISTRIBUTIONS="tau_pt tau_n_tracks"



${CONTRIB}/plot-fake-composition.py \
  --output results_mutau/composition/nominal \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --label 'Nominal, 77% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-00/"

${CONTRIB}/plot-fake-composition.py \
  --output results_mutau/composition/no_btag  \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --label 'Tau b-tag veto, 77% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-01/"

${CONTRIB}/plot-fake-composition.py \
  --output results_mutau/composition/tight \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --label 'Tighter, 70% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-02/"

${CONTRIB}/plot-fake-composition.py \
  --output results_mutau/composition/loose \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --label 'Looser, 85% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-03/"
