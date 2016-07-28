"""Regions for the mu+tau analysis.
"""

# System imports
from functools import partial
from copy import copy

# owls-hep imports
from owls_hep.region import Region
from owls_hep.module import definitions as global_definitions
from owls_hep.expression import expression_substitute

configuration = global_definitions()
year = configuration.get('year', '')

# Set up definitions
definitions = {
    # Global weight
    'weight': '',

    # MC weight
    'weight_mc': 'weight_mc',

    # Pileup weight
    # 'weight_pileup': 'weight_pileup_hash',
    'weight_pileup': 'NOMINAL_pileup_combined_weight',


    # Weight for events with b-jet or b-jet veto
    'weight_b': ('jet_NOMINAL_global_effSF_JVT * '
        'jet_NOMINAL_global_effSF_MVX*jet_NOMINAL_global_ineffSF_MVX'),
        # 'jet_NOMINAL_global_effSF_MVX'),

    # Weights for events with muons
    'weight_mu': (
        'lep_0_NOMINAL_MuEffSF_Reco_QualMedium * '
        'lep_0_NOMINAL_MuEffSF_IsoGradient'
    ),
    'weight_mu_noiso': (
        'lep_0_NOMINAL_MuEffSF_Reco_QualMedium'
    ),
    'weight_mu_trigger_2015': (
                'lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoGradient'
    ),
    'weight_mu_trigger_2016': (
                'lep_0_NOMINAL_MuEffSF_HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoGradient'
    ),

    # Weight for events with taus
    'weight_tau_loose': (
        # 'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron * '
        'tau_0_NOMINAL_TauEffSF_JetBDTloose * '
        'tau_0_NOMINAL_TauEffSF_reco * '
        'tau_0_NOMINAL_TauEffSF_selection'
    ),
    'weight_tau_medium': (
        # 'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron'
        'tau_0_NOMINAL_TauEffSF_JetBDTmedium * '
        'tau_0_NOMINAL_TauEffSF_reco  * '
        'tau_0_NOMINAL_TauEffSF_selection'
    ),
    'weight_tau_tight': (
        # 'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron'
        'tau_0_NOMINAL_TauEffSF_JetBDTtight * '
        'tau_0_NOMINAL_TauEffSF_reco  * '
        'tau_0_NOMINAL_TauEffSF_selection'
    ),

    # Muon trigger for 2015 data
    'mu_trigger_2015': (
        '(HLT_mu20_iloose_L1MU15 && muTrigMatch_0_HLT_mu20_iloose_L1MU15) ||'
        '(HLT_mu40 && muTrigMatch_0_HLT_mu40)'
    ),
    'mu_trigger_2016': (
        '(HLT_mu24_imedium && muTrigMatch_0_HLT_mu24_imedium) ||'
        '(HLT_mu50 && muTrigMatch_0_HLT_mu50)'
    ),

    # OS/SS
    'os': 'lephad_qxq == -1',
    'ss': 'lephad_qxq == 1',

    # 1p/3p
    '1p': 'tau_0_n_tracks == 1',
    '3p': 'tau_0_n_tracks == 3',

    # tau triggers
    'tau25': 'HLT_tau25_medium1_tracktwo_resurrected',

    # Isolation WPs
    'iso_gradient': 'lep_0_iso_wp >= 10000',
    'iso_gradient_loose': 'lep_0_iso_wp >= 1000',
    'iso_tight': 'lep_0_iso_wp % 1000 >= 100',
    'iso_medium': 'lep_0_iso_wp % 1000 >= 10',
    'iso_loose': 'lep_0_iso_wp % 1000 >= 1',

    # b-jet requirement and veto
    'bjet': 'n_bjets >= 1',
    '2bjet': 'n_bjets >= 2',
    # 'bjet': 'n_bjets >= 1 && jet_0_mvx_tagged',
    'bveto': 'n_bjets == 0',

    # tau requirement
    'loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_loose',
    'medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_medium',
    'tight_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_tight',

    # mu+tau T&P
    'mu_tau_2015': (
        'n_electrons == 0 && '
        'n_muons == 1 && lep_0_id_medium && lep_0_pt > 22'),
    'mu_tau_2016': (
        'n_electrons == 0 && '
        'n_muons == 1 && lep_0_id_medium && lep_0_pt > 26'),

    # Jet requirement
    '2jets': 'n_jets >= 2',

    # W CR
    'wcr': 'met_reco_et > 30 && lephad_mt_lep0_met > 60',
}

available_tau_triggers = {
    'tau25':  (
        'HLT_tau25_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau25_medium1_tracktwo'
    ),
    'tau35':  (
        'HLT_tau35_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau35_medium1_tracktwo'
    ),
    'tau80':  (
        'HLT_tau80_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau80_medium1_tracktwo'
    ),
    'tau125': (
        'HLT_tau125_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau125_medium1_tracktwo'
    ),
    'tau160': (
        'HLT_tau160_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau160_medium1_tracktwo'
    ),
}

if year == '2015':
    definitions['mu_trigger'] = definitions['mu_trigger_2015']
    definitions['weight_mu_trigger'] = definitions['weight_mu_trigger_2015']
    definitions['mu_tau'] = definitions['mu_tau_2015']
elif year == '2016':
    definitions['mu_trigger'] = definitions['mu_trigger_2016']
    definitions['weight_mu_trigger'] = definitions['weight_mu_trigger_2016']
    definitions['mu_tau'] = definitions['mu_tau_2016']
else:
    raise RuntimeError('Don\'t know how to handle unknown year "{}.'. \
                       format(year))

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
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

_vary_me('mu_tau_loose_id',
         '[mu_trigger] && [mu_tau] && [loose_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         'Loose #tau',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_b] * [weight_tau_loose]')},
         {'rqcd': 'mu_tau_qcd_cr_loose_id'},
         _variations)

_vary_me('mu_tau_medium_id',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         'Medium #tau',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr_medium_id'},
         _variations)

_vary_me('mu_tau_tight_id',
         '[mu_trigger] && [mu_tau] && [tight_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         'Tight #tau',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_b] * [weight_tau_tight]')},
         {'rqcd': 'mu_tau_qcd_cr_tight_id'},
         _variations)

# QCD CR with anti-isolation
_vary_me('mu_tau_qcd_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * [weight_mu_trigger] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

_vary_me('mu_tau_qcd_cr_loose_id',
         expr('[mu_trigger] && [mu_tau] && [loose_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (loose)',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * [weight_mu_trigger] * [weight_tau_loose]')},
         {'rqcd': 'mu_tau_qcd_cr_loose_id'},
         _variations)

_vary_me('mu_tau_qcd_cr_medium_id',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (medium)',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * [weight_mu_trigger] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr_medium_id'},
         _variations)

_vary_me('mu_tau_qcd_cr_tight_id',
         expr('[mu_trigger] && [mu_tau] && [tight_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (tight)',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * [weight_mu_trigger] * [weight_tau_tight]')},
         {'rqcd': 'mu_tau_qcd_cr_tight_id'},
         _variations)

# QCD CR with isolation
_vary_me('mu_tau_iso_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [iso_gradient]'),
         expr('[weight]'),
         'Isolation CR',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# W CR
_vary_me('mu_tau_w_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && [wcr] && [iso_gradient]'),
         expr('[weight]'),
         'W CR',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# ttbar CR
_vary_me('mu_tau_ttbar_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2bjet] && [iso_gradient]'),
         expr('[weight]'),
         't#bar{t} CR',
         {'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * [weight_mu_trigger] * [weight_b] * [weight_tau_medium]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)
