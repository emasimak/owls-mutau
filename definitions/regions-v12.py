# encoding: utf-8
"""Regions for the mu+tau analysis.
"""

# System imports
from functools import partial
from copy import copy

# owls-hep imports
from owls_hep.region import Region
from owls_hep.module import definitions as global_definitions
from owls_hep.expression import expression_substitute
from owls_hep.variations import ReplaceWeight

configuration = global_definitions()
year = configuration.get('year', None)
tau_pt = configuration.get('tau_pt', None)

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
        'jet_NOMINAL_global_effSF_MVX'),
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
    'weight_tau_very_loose': (
        'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron * '
        'tau_0_NOMINAL_TauEffSF_reco'
    ),
    'weight_tau_loose': (
        'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron * '
        'tau_0_NOMINAL_TauEffSF_JetBDTloose * '
        'tau_0_NOMINAL_TauEffSF_reco'
    ),
    'weight_tau_medium': (
        'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron * '
        'tau_0_NOMINAL_TauEffSF_JetBDTmedium * '
        'tau_0_NOMINAL_TauEffSF_reco'
    ),
    'weight_tau_tight': (
        'tau_0_NOMINAL_TauEffSF_VeryLooseLlhEleOLR_electron * '
        'tau_0_NOMINAL_TauEffSF_JetBDTtight * '
        'tau_0_NOMINAL_TauEffSF_reco'
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
    '1bjet': 'n_bjets == 1',
    '2bjet': 'n_bjets >= 2',
    'bveto': 'n_bjets == 0',

    # tau requirement
    'very_loose_tau': 'n_taus >= 1 && tau_0_jet_bdt_score > 0.3',
    'loose_tau': 'n_taus >= 1 && tau_0_jet_bdt_loose',
    'medium_tau': 'n_taus >= 1 && tau_0_jet_bdt_medium',
    'tight_tau': 'n_taus >= 1 && tau_0_jet_bdt_tight',
    'tau_pt': 'tau_0_pt > 25',
    # 'tau_pt': 'tau_0_pt > 60',

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
        'tau_0_trig_HLT_tau25_medium1_tracktwo',
        'HLT tau25 medium trigger',
    ),
    'tau35':  (
        'HLT_tau35_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau35_medium1_tracktwo',
        'HLT tau35 medium trigger',
    ),
    'tau50_L1TAU12':  (
        'HLT_tau50_medium1_tracktwo_L1TAU12_resurrected',
        'tau_0_trig_HLT_tau50_medium1_tracktwo_L1TAU12',
        'HLT tau50 (L1 TAU12) medium trigger',
    ),
    'tau80':  (
        'HLT_tau80_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau80_medium1_tracktwo',
        'HLT tau80 medium trigger',
    ),
    'tau80_L1TAU60':  (
        'HLT_tau80_medium1_tracktwo_L1TAU60_resurrected',
        'tau_0_trig_HLT_tau80_medium1_tracktwo_L1TAU60',
        'HLT tau80 (L1 TAU60) medium trigger',
    ),
    'tau125': (
        'HLT_tau125_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau125_medium1_tracktwo',
        'HLT tau125 medium trigger',
    ),
    'tau160': (
        'HLT_tau160_medium1_tracktwo_resurrected',
        'tau_0_trig_HLT_tau160_medium1_tracktwo',
        'HLT tau160 medium trigger',
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

label_addon = ''
rqcd_addon = ''
if tau_pt is not None:
    definitions['tau_pt'] = 'tau_0_pt > {}'.format(tau_pt)
    label_addon = ' (#tau p_{{T}} > {} GeV)'.format(tau_pt)
    rqcd_addon = '_tau{}'.format(tau_pt)

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
        m['rqcd'] = m['rqcd'] + v[5]
        if isinstance(label, basestring):
            l = [label + v[3]]
        else:
            l = [label[0] + v[3]] + list(label[1:])
        if isinstance(v[4], tuple) or isinstance(v[4], list):
            l += list(v[4])
        else:
            l.append(v[4])
        globals()[name + v[0]] = Region(expr(selection + v[1]),
                                        expr(weight + v[2]),
                                        l,
                                        patches,
                                        metadata = m)

# mu+tau region and variations for publishing
_variations = [
    #(name_addon, selection_addon, weight_addon, label, rqcd_addon)
    ('_1p',        '&& [1p]',             '',  '',  '1-track',                                '_1p'),
    ('_3p',        '&& [3p]',             '',  '',  '3-track',                                '_3p'),
    ('_tau25',     '&& [tau25]',          '',  '',  'HLT tau25 medium trigger',               '_tau25'),
    ('_tau25_1p',  '&& [tau25] && [1p]',  '',  '',  ['1-track', 'HLT tau25 medium trigger'],  '_tau25_1p'),
    ('_tau25_3p',  '&& [tau25] && [3p]',  '',  '',  ['3-track', 'HLT tau25 medium trigger'],  '_tau25_3p'),
]

_vary_me('mu_tau_publish',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         't#bar{t} #rightarrow #mu#tau_{had} T&P',
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)

_vary_me('ttbar_cr_publish',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         ('t#bar{t} #rightarrow #mu#tau_{had} T&P', '≥ 2 b-jet selection'),
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)


# Nominal mu+tau region and variations
_variations = [
    #(name_addon, selection_addon, weight_addon, label, rqcd_addon)
    ('_tau25',        '&& [tau25]',                  '',  '',                'HLT_tau25_medium1_tracktwo',  '_tau25'),
    ('_tau25_1p',     '&& [tau25] && [1p]',          '',  ' (1-prong)',      'HLT_tau25_medium1_tracktwo',  '_tau25_1p'),
    ('_tau25_3p',     '&& [tau25] && [3p]',          '',  ' (3-prong)',      'HLT_tau25_medium1_tracktwo',  '_tau25_3p'),
    ('_tau25_os',     '&& [tau25] && [os]',          '',  ' (OS)',           'HLT_tau25_medium1_tracktwo',  ''),
    ('_tau25_ss',     '&& [tau25] && [ss]',          '',  ' (SS)',           'HLT_tau25_medium1_tracktwo',  ''),
    ('_tau25_1p_os',  '&& [tau25] && [os] && [1p]',  '',  ' (1-prong, OS)',  'HLT_tau25_medium1_tracktwo',  ''),
    ('_tau25_1p_ss',  '&& [tau25] && [ss] && [1p]',  '',  ' (1-prong, SS)',  'HLT_tau25_medium1_tracktwo',  ''),
    ('_tau25_3p_os',  '&& [tau25] && [os] && [3p]',  '',  ' (3-prong, OS)',  'HLT_tau25_medium1_tracktwo',  ''),
    ('_tau25_3p_ss',  '&& [tau25] && [ss] && [3p]',  '',  ' (3-prong, SS)',  'HLT_tau25_medium1_tracktwo',  ''),
    ('_1p',           '&& [1p]',                     '',  ' (1-prong)',      None,                          '_1p'),
    ('_3p',           '&& [3p]',                     '',  ' (3-prong)',      None,                          '_3p'),
    ('_os',           '&& [os]',                     '',  ' (OS)',           None,                          ''),
    ('_ss',           '&& [ss]',                     '',  ' (SS)',           None,                          ''),
    ('_1p_os',        '&& [os] && [1p]',             '',  ' (1-prong, OS)',  None,                          ''),
    ('_1p_ss',        '&& [ss] && [1p]',             '',  ' (1-prong, SS)',  None,                          ''),
    ('_3p_os',        '&& [os] && [3p]',             '',  ' (3-prong, OS)',  None,                          ''),
    ('_3p_ss',        '&& [ss] && [3p]',             '',  ' (3-prong, SS)',  None,                          ''),
]

_vary_me('mu_tau',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         '#mu+#tau' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)

_vary_me('mu_tau_very_loose',
         '[mu_trigger] && [mu_tau] && [very_loose_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         '#tau BDT > 0.3' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_very_loose]')
         },
         {'rqcd': 'qcd_cr_loose' + rqcd_addon},
         _variations)

_vary_me('mu_tau_loose',
         '[mu_trigger] && [mu_tau] && [loose_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         'Loose #tau' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_loose]')
         },
         {'rqcd': 'qcd_cr_loose' + rqcd_addon},
         _variations)

_vary_me('mu_tau_medium',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         'Medium #tau' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr_medium' + rqcd_addon},
         _variations)

_vary_me('mu_tau_tight',
         '[mu_trigger] && [mu_tau] && [tight_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         'Tight #tau' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_tight]')
         },
         {'rqcd': 'qcd_cr_tight' + rqcd_addon},
         _variations)

# QCD CR with anti-isolation
_vary_me('qcd_cr',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && ![iso_gradient]',
         '[weight]',
         'QCD CR' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)

_vary_me('qcd_cr_very_loose',
         '[mu_trigger] && [mu_tau] && [very_loose_tau] && [tau_pt] && [2jets] && '
         '[bjet] && ![iso_gradient]',
         '[weight]',
         'QCD CR (very loose)' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_very_loose]')
         },
         {'rqcd': 'qcd_cr_very_loose' + rqcd_addon},
         _variations)

_vary_me('qcd_cr_loose',
         '[mu_trigger] && [mu_tau] && [loose_tau] && [tau_pt] && [2jets] && '
         '[bjet] && ![iso_gradient]',
         '[weight]',
         'QCD CR (loose)' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_loose]')
         },
         {'rqcd': 'qcd_cr_loose' + rqcd_addon},
         _variations)

_vary_me('qcd_cr_medium',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && ![iso_gradient]',
         '[weight]',
         'QCD CR (medium)' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr_medium' + rqcd_addon},
         _variations)

_vary_me('qcd_cr_tight',
         '[mu_trigger] && [mu_tau] && [tight_tau] && [tau_pt] && [2jets] && '
         '[bjet] && ![iso_gradient]',
         '[weight]',
         'QCD CR (tight)' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu_noiso] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_tight]')
         },
         {'rqcd': 'qcd_cr_tight' + rqcd_addon},
         _variations)

# QCD CR with isolation
_vary_me('qcd_iso_cr',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[bjet] && [iso_gradient]',
         '[weight]',
         'Isolation CR' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)

# W CR
_vary_me('w_cr',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [bveto] && '
         '[wcr] && [iso_gradient]',
         '[weight]',
         'W CR' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)

# ttbar CR
_vary_me('ttbar_cr',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[2bjet] && [iso_gradient]',
         '[weight]',
         't#bar{t} CR' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)

_vary_me('1bjet_cr',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [tau_pt] && [2jets] && '
         '[1bjet] && [iso_gradient]',
         '[weight]',
         '1 b-jet CR' + label_addon,
         {
             'mc': expr('[weight_mc] * [weight_pileup] * [weight_mu] * '
                        '[weight_mu_trigger] * [weight_b] * '
                        '[weight_tau_medium]')
         },
         {'rqcd': 'qcd_cr' + rqcd_addon},
         _variations)
