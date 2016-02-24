"""Regions for the tau+jets analysis.
"""

# System imports
from functools import partial
from copy import copy

# owls-hep imports
from owls_hep.region import Region
from owls_hep.expression import expression_substitute

# Set up definitions
definitions = {
    # General weight
    'weight': 'weight_mc',
    'weight_pileup': 'weight_pileup_hash',

    # Weight for events with b-jet or b-jet veto
    'weight_b': ('btag_NOMINAL_global_effSF_MVX * '
                 'btag_NOMINAL_global_ineffSF_MVX'),

    # Weights for events with muons
    'weight_mu': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_effSF_IsoGradient * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_NONE'
    ),
    'weight_mu_noiso': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_NONE'
    ),
    'weight_mu_loose': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_effSF_IsoLoose * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_LOOSE'
    ),
    'weight_mu_tight': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_effSF_IsoTight * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_TIGHT'
    ),

    # Weight for events with taus
    'weight_tau': (
        'tau_0_NOMINAL_TAU_EFF_ELEOLR * '
        'tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM * '
        'tau_0_NOMINAL_TAU_EFF_RECO * '
        'tau_0_NOMINAL_TAU_EFF_SELECTION'
    ),

    # Overrides
    #'weight_pileup': 'weight_pileup',
    #'weight_b': '1',
    #'weight_mu': '1',
    #'weight_tau': '1',

    # Muon trigger for 2015 data
    'mu_trigger': (
        '(HLT_mu20_iloose_L1MU15 && muTrigMatch_0_HLT_mu20_iloose_L1MU15)'),

    # OS/SS
    'os': 'lephad_qxq == -1',
    'ss': 'lephad_qxq == 1',

    # 1p/3p
    '1p': 'tau_0_n_tracks == 1',
    '3p': 'tau_0_n_tracks == 3',

    # tau triggers
    'tau25': 'HLT_tau25_medium1_tracktwo && tau_0_trig_HLT_tau25_medium1_tracktwo',
    'tau35': 'HLT_tau35_medium1_tracktwo && tau_0_trig_HLT_tau35_medium1_tracktwo',

    # Old isolation
    'iso_old': (
        'lep_0_iso_ptcone40/1000.0/lep_0_pt < 0.01 && '
        'lep_0_iso_etcone20/1000.0/lep_0_pt < 0.04'),
    'iso_old_loose': (
        'lep_0_iso_ptcone40/1000.0/lep_0_pt < 0.10 && '
        'lep_0_iso_etcone20/1000.0/lep_0_pt < 0.13'),

    # Isolation WPs
    'iso_gradient': 'lep_0_iso_wp >= 10000',
    'iso_gradient_loose': 'lep_0_iso_wp >= 1000',
    'iso_tight': 'lep_0_iso_wp % 1000 >= 100',
    'iso_medium': 'lep_0_iso_wp % 1000 >= 10',
    'iso_loose': 'lep_0_iso_wp % 1000 >= 1',

    # b-jet requirement and veto
    '2bjet': 'n_bjets >= 2',
    '1bjet': 'n_bjets == 1',
    'bjet': 'n_bjets >= 1',
    'bveto': 'n_bjets == 0',

    # tau requirement
    'loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_loose',
    'medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_medium',
    'tight_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_tight',

    'anti_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_score > 0.5 && !tau_0_jet_bdt_loose',

    # mu+tau T&P
    'mu_tau': (
        'n_electrons == 0 && '
        'n_muons == 1 && lep_0_id_medium && lep_0_pt > 22'),

    # Jet requirement
    '2jets': 'n_jets >= 2',

    # W CR
    'wcr': 'met_reco_et > 30 && lephad_mt_lep0_met > 60',
}

expr = partial(expression_substitute, definitions = definitions)

def _vary_me(name, selection, weight, label, patches, metadata, variations):
    if not name in globals():
        globals()[name] = Region(expr(selection),
                                 expr(weight),
                                 label,
                                 patches,
                                 metadata = metadata)
    for v in variations:
        m = copy(metadata)
        m.update(v[4])
        globals()[name + v[0]] = Region(expr(selection + v[1]),
                                        expr(weight + v[2]),
                                        label + v[3],
                                        patches,
                                        metadata = m)

# mu+tau regions
_variations = [
    ('_tau25', '&& [tau25]', '', ' (tau25)', {}),
    ('_tau25_1p', '&& [tau25] && [1p]', '', ' (tau25, 1-prong)', {'rqcd': 'mu_tau_qcd_cr_1p'}),
    ('_tau25_3p', '&& [tau25] && [3p]', '', ' (tau25, 3-prong)', {'rqcd': 'mu_tau_qcd_cr_3p'}),
    ('_tau25_os', '&& [tau25] && [os]', '', ' (tau25, OS)', {}),
    #('_tau25_ss', '&& [tau25] && [ss]', '', ' (tau25, SS)', {}),
    ('_1p', '&& [1p]', '', ' (1-prong)', {'rqcd': 'mu_tau_qcd_cr_1p'}),
    ('_3p', '&& [3p]', '', ' (3-prong)', {'rqcd': 'mu_tau_qcd_cr_3p'}),
    ('_os', '&& [os]', '', ' (OS)', {}),
    ('_ss', '&& [ss]', '', ' (SS)', {}),
]

# Nominal mu+tau region and variations
_vary_me('mu_tau',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         '#mu+#tau',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

_vary_me('mu_tau_gradient',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         '#mu+#tau (Gradient)',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

_vary_me('mu_tau_loose',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_loose]',
         '[weight]',
         '#mu+#tau (Loose)',
         {'mc': expr('[weight_pileup] * [weight_mu_loose] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

_vary_me('mu_tau_tight',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_tight]',
         '[weight]',
         '#mu+#tau (Tight)',
         {'mc': expr('[weight_pileup] * [weight_mu_tight] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# mu+tau region and variations without isolation cut
_vary_me('mu_tau_noiso',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet]',
         '[weight]',
         '#mu+#tau',
         {'mc': expr('[weight_pileup] * [weight_mu_noiso] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# QCD CR with anti-isolation
_vary_me('mu_tau_qcd_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR',
         {'mc': expr('[weight_pileup] * [weight_mu]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# W CR
_vary_me('mu_tau_w_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && [wcr] && [iso_gradient]'),
         expr('[weight]'),
         'W CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# ttbar CR
_vary_me('mu_tau_ttbar_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [2bjet] && [iso_gradient]'),
         expr('[weight]'),
         '2b CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# ttbar CR loose
_vary_me('mu_tau_loose_ttbar_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [2bjet] && [iso_loose]'),
         expr('[weight]'),
         '2b CR',
         {'mc': expr('[weight_pileup] * [weight_mu_loose] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# ttbar CR
_vary_me('mu_tau_1b_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [1bjet] && [iso_gradient]'),
         expr('[weight]'),
         '1b CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)
