#!/usr/bin/env sh

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
REGIONS="\
  mu_tau_os mu_tau_tau25_os \
  mu_tau_ttbar_cr_os mu_tau_ttbar_cr_tau25_os \
  mu_tau_1b_cr_os \
  "
DISTRIBUTIONS="tau_pt tau_n_tracks"



"$OWLS/tools/plot-fake-composition.py" \
  --output results/composition/nominal \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models.py" \
  --regions-file "$OWLS/definitions/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label 'Nominal, 77% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-00/"

"$OWLS/tools/plot-fake-composition.py" \
  --output results/composition/no_btag  \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models.py" \
  --regions-file "$OWLS/definitions/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label 'Tau b-tag veto, 77% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-01/"

"$OWLS/tools/plot-fake-composition.py" \
  --output results/composition/tight \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models.py" \
  --regions-file "$OWLS/definitions/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label 'Tighter, 70% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-02/"

"$OWLS/tools/plot-fake-composition.py" \
  --output results/composition/loose \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models.py" \
  --regions-file "$OWLS/definitions/regions.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label 'Looser, 85% eff' \
  data_prefix="/disk/d3/ohman/tagprobe_v01-X-03_merged/v01-03/"
