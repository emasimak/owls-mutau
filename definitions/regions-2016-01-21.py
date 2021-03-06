"""Regions for the mu+tau analysis.
"""

# System imports
from functools import partial
from copy import copy

# owls-hep imports
from owls_hep.region import Region
from owls_hep.expression import expression_substitute

# Set up definitions
definitions = {
    # MC weight
    'weight': 'weight_mc',

    # Pileup weight
    'weight_pileup': 'weight_pileup_hash',

    # Weight for events with b-jet or b-jet veto
    'weight_b': 'bjet_sf_MVX_NOMINAL_sf',

    # Weights for events with muons
    'weight_mu': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_effSF_IsoGradient * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'
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
    'weight_tau_loose': (
        'tau_0_NOMINAL_TAU_EFF_ELEOLR * '
        'tau_0_NOMINAL_TAU_EFF_JETIDBDTLOOSE * '
        'tau_0_NOMINAL_TAU_EFF_RECO'
    ),
    'weight_tau_medium': (
        'tau_0_NOMINAL_TAU_EFF_ELEOLR * '
        'tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM * '
        'tau_0_NOMINAL_TAU_EFF_RECO'
    ),
    'weight_tau_tight': (
        'tau_0_NOMINAL_TAU_EFF_ELEOLR * '
        'tau_0_NOMINAL_TAU_EFF_JETIDBDTTIGHT * '
        'tau_0_NOMINAL_TAU_EFF_RECO'
    ),

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

available_tau_triggers = {
    'tau25':  (
        'HLT_tau25_medium1_tracktwo',
        'tau_0_trig_HLT_tau25_medium1_tracktwo',
        'HLT tau25 medium trigger',
    ),
    'tau35':  (
        'HLT_tau35_medium1_tracktwo',
        'tau_0_trig_HLT_tau35_medium1_tracktwo',
        'HLT tau35 medium trigger',
    ),
    'tau80':  (
        'HLT_tau80_medium1_tracktwo',
        'tau_0_trig_HLT_tau80_medium1_tracktwo',
        'HLT tau80 medium trigger',
    ),
    'tau125': (
        'HLT_tau125_medium1_tracktwo',
        'tau_0_trig_HLT_tau125_medium1_tracktwo',
        'HLT tau125 medium trigger',
    ),
    'tau160': (
        'HLT_tau160_medium1_tracktwo',
        'tau_0_trig_HLT_tau160_medium1_tracktwo',
        'HLT tau160 medium trigger',
    ),
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
        m['rqcd'] = m['rqcd'] + v[4]
        globals()[name + v[0]] = Region(expr(selection + v[1]),
                                        expr(weight + v[2]),
                                        label + v[3],
                                        patches,
                                        metadata = m)

# mu+tau regions
_variations = [
    #(name_addon, selection_addon, weight_addon, rqcd_addon,
    ('_tau25', '&& [tau25]', '', ' (tau25)', '_tau25'),
    ('_tau25_1p', '&& [tau25] && [1p]', '', ' (tau25, 1-prong)', '_tau25_1p'),
    ('_tau25_3p', '&& [tau25] && [3p]', '', ' (tau25, 3-prong)', '_tau25_3p'),
    ('_tau25_os', '&& [tau25] && [os]', '', ' (tau25, OS)', ''),
    ('_tau25_ss', '&& [tau25] && [ss]', '', ' (tau25, SS)', ''),
    ('_tau25_1p_os', '&& [tau25] && [os] && [1p]', '', ' (tau25, 1-prong, OS)', ''),
    ('_tau25_1p_ss', '&& [tau25] && [ss] && [1p]', '', ' (tau25, 1-prong, SS)', ''),
    ('_tau25_3p_os', '&& [tau25] && [os] && [3p]', '', ' (tau25, 3-prong, OS)', ''),
    ('_tau25_3p_ss', '&& [tau25] && [ss] && [3p]', '', ' (tau25, 3-prong, SS)', ''),
    ('_1p', '&& [1p]', '', ' (1-prong)', '_1p'),
    ('_3p', '&& [3p]', '', ' (3-prong)', '_3p'),
    ('_os', '&& [os]', '', ' (OS)', ''),
    ('_ss', '&& [ss]', '', ' (SS)', ''),
    ('_1p_os', '&& [os] && [1p]', '', ' (1-prong, OS)', ''),
    ('_1p_ss', '&& [ss] && [1p]', '', ' (1-prong, SS)', ''),
    ('_3p_os', '&& [os] && [3p]', '', ' (3-prong, OS)', ''),
    ('_3p_ss', '&& [ss] && [3p]', '', ' (3-prong, SS)', ''),
]

# Nominal mu+tau region and variations
_vary_me('mu_tau',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         '#mu+#tau',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_medium]')},
         # {'mc': expr('[weight_mu] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

_vary_me('mu_tau_loose',
         '[mu_trigger] && [mu_tau] && [loose_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         'Loose #tau',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_loose]')},
         {'rqcd': 'qcd_cr_loose'},
         _variations)

_vary_me('mu_tau_medium',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         'Medium #tau',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr_medium'},
         _variations)

_vary_me('mu_tau_tight',
         '[mu_trigger] && [mu_tau] && [tight_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         'Tight #tau',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_tight]')},
         {'rqcd': 'qcd_cr_tight'},
         _variations)

_vary_me('iso_gradient',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         '#mu+#tau (Gradient iso)',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

_vary_me('iso_loose',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_loose]',
         '[weight]',
         '#mu+#tau (Loose iso)',
         {'mc': expr('[weight_pileup] * [weight_mu_loose] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

_vary_me('iso_tight',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_tight]',
         '[weight]',
         '#mu+#tau (Tight iso)',
         {'mc': expr('[weight_pileup] * [weight_mu_tight] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

# mu+tau region and variations without isolation cut
_vary_me('noiso_cr',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets]',
         '[weight]',
         'No isolation CR',
         {'mc': expr('[weight_pileup] * [weight_mu_noiso] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

# QCD CR with anti-isolation
_vary_me('qcd_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR',
         {'mc': expr('[weight_pileup] * [weight_mu_noiso] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

_vary_me('qcd_cr_loose',
         expr('[mu_trigger] && [mu_tau] && [loose_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (loose)',
         {'mc': expr('[weight_pileup] * [weight_mu_noiso] * [weight_tau_loose]')},
         {'rqcd': 'qcd_cr_loose'},
         _variations)

_vary_me('qcd_cr_medium',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (medium)',
         {'mc': expr('[weight_pileup] * [weight_mu_noiso] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr_medium'},
         _variations)

_vary_me('qcd_cr_tight',
         expr('[mu_trigger] && [mu_tau] && [tight_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (tight)',
         {'mc': expr('[weight_pileup] * [weight_mu_noiso] * [weight_tau_tight]')},
         {'rqcd': 'qcd_cr_tight'},
         _variations)

# QCD CR with isolation
_vary_me('iso_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [iso_gradient]'),
         expr('[weight]'),
         'Isolation CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

# W CR
_vary_me('w_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && [wcr] && [iso_gradient]'),
         expr('[weight]'),
         'W CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

# ttbar CR
_vary_me('ttbar_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [2bjet] && [iso_gradient]'),
         expr('[weight]'),
         '2b CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)

# 1b CR
_vary_me('1b_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [1bjet] && [iso_gradient]'),
         expr('[weight]'),
         '1b CR',
         {'mc': expr('[weight_pileup] * [weight_mu] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'qcd_cr'},
         _variations)
