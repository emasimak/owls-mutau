"""Regions for the tau+jets analysis.
"""

# System imports
from functools import partial

# owls-hep imports
from owls_hep.region import Region
from owls_hep.expression import expression_substitute

# Set up definitions
definitions = {
    # General weight
    'weight': 'weight_mc*weight_pileup',
    #'weight': 'weight_mc',

    # Weight for events with b-jet or b-jet veto
    'weight_b': 'bjets_sf*bjets_ineff_sf',

    # Weights for events with muons
    'weight_mu': (
        'lep_0_NOMINAL_MU_RECO_MEDIUM * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_NONE'
    ),

    # Muon trigger for 2015 data
    'mu_trigger': (
        '(HLT_mu20_iloose_L1MU15 && muTrigMatch_0_HLT_mu20_iloose_L1MU15)'),

    # OS/SS for mu+tau selection
    'os': 'lephad_qxq == -1',
    'ss': 'lephad_qxq == 1',

    # Isolation
    'isolation': (
        'lep_0_iso_ptcone40/lep_0_pt < 0.01 && '
        'lep_0_iso_etcone20/lep_0_pt < 0.04'),

    # b-jet requirement and veto
    'bjet': 'n_bjets >= 1',
    'bveto': 'n_bjets == 0',

    # tau requirement
    'loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_loose',
    'medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_medium',
    'tight_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_tight',
    'not_loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_loose',
    'loose_not_medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_loose && !tau_0_jet_bdt_medium',
    'very_loose_not_medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_score > 0.5 && !tau_0_jet_bdt_medium',
    'very_loose_not_loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_score > 0.5 && !tau_0_jet_bdt_loose',

    # mu+tau T&P
    'mu_tau': (
        'n_jets >= 2 && '
        'n_electrons == 0 && '
        'n_muons == 1 && lep_0_id_medium && lep_0_pt > 22'),

    # More jets
    '3jets': 'n_jets >= 3',

    # W CR
    'wcr': 'met_reco_et > 30 && lephad_mt_lep0_met > 60',
}

expr = partial(expression_substitute, definitions = definitions)

def _vary_me(name, selection, weight, label, metadata, variations):
    if not name in globals():
        globals()[name] = Region(expr(selection),
                                 expr(weight),
                                 label,
                                 metadata = metadata)
    for v in variations:
        globals()[name + v[0]] = Region(expr(selection + v[1]),
                                        expr(weight + v[2]),
                                        label + v[3],
                                        metadata = metadata)


_id_variations = [
    ('_loose', '&& tau_0_jet_bdt_loose', '', ' (loose #tau)'),
    ('_medium', '&& tau_0_jet_bdt_medium', '', ' (medium #tau)'),
    ('_tight', '&& tau_0_jet_bdt_tight', '', ' (tight #tau)'),
]

# mu+tau regions
_variations = [
    ('_tau25', '&& HLT_tau25_medium1_tracktwo', '', ' (tau25)'),
    ('_tau35', '&& HLT_tau35_medium1_tracktwo', '', ' (tau35)'),
    ('_tau25_os', '&& [os] && HLT_tau25_medium1_tracktwo', '', ' (tau25, OS)'),
    ('_tau35_os', '&& [os] && HLT_tau35_medium1_tracktwo', '', ' (tau35, OS)'),
    ('_1p', '&& tau_0_n_tracks == 1', '', ' (1-prong)'),
    ('_3p', '&& tau_0_n_tracks == 3', '', ' (3-prong)'),
    ('_os', '&& [os]', '', ' (OS)'),
    ('_ss', '&& [ss]', '', ' (SS)'),
]

#qcd_cr = Region(
    #expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && ![isolation]'),
    #expr('[weight] * [weight_b]'),
    #'QCD CR',
    #{'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'}
#)

#mu_tau = Region(
    #expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && [isolation]'),
    #expr('[weight] * [weight_b]'),
    #'#mu+#tau',
    #{'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'}
#)

mu_tau_qcd_cr1 = Region(
    expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bjet] && [isolation]'),
    expr('[weight] * [weight_b]'),
    '#mu+#tau (bdt > 0.5 && !loose && bveto)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'qcd_cr1'}
)

mu_tau_qcd_cr2 = Region(
    expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bjet] && [isolation]'),
    expr('[weight] * [weight_b]'),
    '#mu+#tau (bdt > 0.5 && !medium && bveto)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'qcd_cr2'}
)

mu_tau_qcd_cr3 = Region(
    expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bjet] && [isolation]'),
    expr('[weight] * [weight_b]'),
    '#mu+#tau (medium && bveto)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'qcd_cr3'}
)

qcd_cr1 = Region(
    expr('[mu_trigger] && [mu_tau] && [very_loose_not_loose_tau] && [bveto] && ![isolation]'),
    expr('[weight] * [weight_b]'),
    'QCD CR (bdt > 0.5 && !loose && bveto)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'}
)

qcd_cr2 = Region(
    expr('[mu_trigger] && [mu_tau] && [very_loose_not_medium_tau] && [bveto] && ![isolation]'),
    expr('[weight] * [weight_b]'),
    'QCD CR (bdt > 0.5 && !medium && bveto)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'}
)

qcd_cr3 = Region(
    expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && ![isolation]'),
    expr('[weight] * [weight_b]'),
    'QCD CR (medium && bveto)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'}
)

qcd_cr4 = Region(
    expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bjet] && ![isolation]'),
    expr('[weight] * [weight_b]'),
    'QCD CR (medium && btag)',
    {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'}
)

# Nominal mu+tau region and variations
_vary_me('mu_tau',
         '[mu_tau] && [mu_trigger] && [medium_tau] && [bjet] && [isolation]',
         '[weight] * [weight_b]',
         '#mu+#tau',
         {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'},
         _variations)

# Nominal QCD CR and variations
_vary_me('mu_tau_qcd_cr',
         expr('[mu_trigger] && [mu_tau] && [very_loose_not_medium_tau] && [bveto] && ![isolation]'),
         expr('[weight] * [weight_b]'),
         'QCD CR',
         {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'},
         _variations)

# Nominal W CR and variations
_vary_me('mu_tau_w_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && [wcr] && [isolation]'),
         expr('[weight] * [weight_b]'),
         'W CR',
         {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'},
         _variations)

_vary_me('mu_tau_fake_cr',
         expr('[mu_trigger] && [mu_tau] && [very_loose_not_loose_tau] && [bjet] && [3jets] && [isolation]'),
         expr('[weight] * [weight_b]'),
         'Jet fake CR (bdt > 0.5 && !loose)',
         {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'},
         _variations)

_vary_me('mu_tau_fake_cr2',
         expr('[mu_trigger] && [mu_tau] && [very_loose_not_medium_tau] && [bjet] && [3jets] && [isolation]'),
         expr('[weight] * [weight_b]'),
         'Jet fake CR (bdt > 0.5 && !medium)',
         {'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'},
         _variations)

# mu+tau region with ID variations
#_vary_me('mu_tau',
         #'[mu_tau] && [mu_trigger]',
         #'[weight]*[weight_mu]',
         #'#mu+#tau',
         #{'weight': {'mc': expr('[weight_mu]')}, 'channel': 'mu_tau'},
         #_id_variations)
