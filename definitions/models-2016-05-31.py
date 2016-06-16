"""Standard data, and background models for the mu+tau analysis.
"""

# System imports
from functools import partial
from collections import OrderedDict
from os.path import join

# Six imports
from six import iterkeys

# owls-hep imports
from owls_hep.process import Patch, Process
from owls_hep.module import definitions
from owls_hep.estimation import Plain, MonteCarlo
from owls_hep.expression import expression_substitute

# owls-mutau imports
from owls_mutau.estimation import OSData, SSData, OSSS
from owls_mutau.uncertainties import TestSystFlat, TestSystShape, \
        MuonEffStat, MuonEffSys, \
        MuonEffTrigStat, MuonEffTrigSys, \
        MuonIsoStat, MuonIsoSys, \
        MuonIdSys, MuonMsSys, MuonScaleSys, \
        RqcdStat, RqcdSyst, \
        BJetEigenB0, BJetEigenB1, BJetEigenB2, BJetEigenB3, BJetEigenB4, \
        BJetEigenC0, BJetEigenC1, BJetEigenC2, BJetEigenC3, \
        BJetEigenLight0, BJetEigenLight1, BJetEigenLight2, BJetEigenLight3, \
        BJetEigenLight4, BJetEigenLight5, BJetEigenLight6, BJetEigenLight7, \
        BJetEigenLight8, BJetEigenLight9, BJetEigenLight10, BJetEigenLight11, \
        BJetEigenLight12, BJetEigenLight13, \
        BJetExtrapolation

# Load configuration
configuration = definitions()
systematics = configuration.get('enable_systematics', '')
data_prefix = configuration.get('data_prefix', '')
luminosity = float(configuration.get('luminosity', 1000.0)) # 1/fb
nominal_tree = 'NOMINAL'
sqrt_s = 13.0 * 1000 * 1000 # MeV

r_qcd = {
    'mu_tau_qcd_cr': [('tau_0_pt <= 40', 1.211, 0.019, 0.063), ('tau_0_pt > 40', 1.372, 0.04, 0.064)],
    'mu_tau_qcd_cr_1p': [('tau_0_pt <= 40', 1.195, 0.022, 0.068), ('tau_0_pt > 40', 1.306, 0.042, 0.065)],
    'mu_tau_qcd_cr_3p': [('tau_0_pt <= 35', 1.241, 0.042, 0.098), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.433, 0.085, 0.092), ('tau_0_pt > 50', 1.993, 0.225, 0.234)],
    'mu_tau_qcd_cr_loose_id': [('tau_0_pt <= 40', 1.154, 0.013, 0.034), ('tau_0_pt > 40', 1.318, 0.029, 0.048)],
    'mu_tau_qcd_cr_loose_id_1p': [('tau_0_pt <= 40', 1.142, 0.017, 0.047), ('tau_0_pt > 40', 1.265, 0.032, 0.051)],
    'mu_tau_qcd_cr_loose_id_3p': [('tau_0_pt <= 35', 1.167, 0.024, 0.04), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.291, 0.048, 0.091), ('tau_0_pt > 50', 1.582, 0.101, 0.12)],
    'mu_tau_qcd_cr_medium_id': [('tau_0_pt <= 40', 1.211, 0.019, 0.063), ('tau_0_pt > 40', 1.372, 0.04, 0.064)],
    'mu_tau_qcd_cr_medium_id_1p': [('tau_0_pt <= 40', 1.195, 0.022, 0.068), ('tau_0_pt > 40', 1.306, 0.042, 0.065)],
    'mu_tau_qcd_cr_medium_id_3p': [('tau_0_pt <= 35', 1.241, 0.042, 0.098), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.433, 0.085, 0.092), ('tau_0_pt > 50', 1.993, 0.225, 0.234)],
    'mu_tau_qcd_cr_tight_id': [('tau_0_pt <= 40', 1.251, 0.029, 0.068), ('tau_0_pt > 40', 1.437, 0.061, 0.055)],
    'mu_tau_qcd_cr_tight_id_1p': [('tau_0_pt <= 40', 1.219, 0.031, 0.078), ('tau_0_pt > 40', 1.377, 0.062, 0.053)],
    'mu_tau_qcd_cr_tight_id_3p': [('tau_0_pt <= 35', 1.372, 0.076, 0.092), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.624, 0.161, 0.188), ('tau_0_pt > 50', 2.026, 0.403, 0.317)],
    'mu_tau_qcd_cr_tau25': [('tau_0_pt <= 40', 1.246, 0.029, 0.082), ('tau_0_pt > 40', 1.45, 0.05, 0.083)],
    'mu_tau_qcd_cr_tau25_1p': [('tau_0_pt <= 40', 1.224, 0.031, 0.086), ('tau_0_pt > 40', 1.384, 0.052, 0.078)],
    'mu_tau_qcd_cr_tau25_3p': [('tau_0_pt <= 35', 1.419, 0.116, 0.142), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.502, 0.117, 0.143), ('tau_0_pt > 50', 2.116, 0.287, 0.271)],
    'mu_tau_qcd_cr_loose_id_tau25': [('tau_0_pt <= 40', 1.205, 0.022, 0.051), ('tau_0_pt > 40', 1.381, 0.037, 0.066)],
    'mu_tau_qcd_cr_loose_id_tau25_1p': [('tau_0_pt <= 40', 1.187, 0.024, 0.063), ('tau_0_pt > 40', 1.314, 0.04, 0.059)],
    'mu_tau_qcd_cr_loose_id_tau25_3p': [('tau_0_pt <= 35', 1.298, 0.07, 0.11), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.363, 0.071, 0.156), ('tau_0_pt > 50', 1.835, 0.153, 0.156)],
    'mu_tau_qcd_cr_medium_id_tau25': [('tau_0_pt <= 40', 1.246, 0.029, 0.082), ('tau_0_pt > 40', 1.45, 0.05, 0.083)],
    'mu_tau_qcd_cr_medium_id_tau25_1p': [('tau_0_pt <= 40', 1.224, 0.031, 0.086), ('tau_0_pt > 40', 1.384, 0.052, 0.078)],
    'mu_tau_qcd_cr_medium_id_tau25_3p': [('tau_0_pt <= 35', 1.419, 0.116, 0.142), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.502, 0.117, 0.143), ('tau_0_pt > 50', 2.116, 0.287, 0.271)],
    'mu_tau_qcd_cr_tight_id_tau25': [('tau_0_pt <= 40', 1.282, 0.041, 0.09), ('tau_0_pt > 40', 1.534, 0.075, 0.079)],
    'mu_tau_qcd_cr_tight_id_tau25_1p': [('tau_0_pt <= 40', 1.262, 0.043, 0.093), ('tau_0_pt > 40', 1.466, 0.076, 0.074)],
    'mu_tau_qcd_cr_tight_id_tau25_3p': [('tau_0_pt <= 35', 1.545, 0.194, 0.224), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.591, 0.195, 0.185), ('tau_0_pt > 50', 2.469, 0.588, 0.473)],
}

# Redefitions of estimations
MonteCarlo = partial(MonteCarlo, luminosity = luminosity)
OSSS = partial(OSSS, r_qcd = r_qcd, luminosity = luminosity)
SSData = partial(SSData, r_qcd = r_qcd)

# Redefitions of uncertainties
# NOTE: This is a cleaner way to initialize the class with an rQCD value than
# invoking partial. When invoking partial, the type of the class is exchanged
# with the partial type. This prevents class comparison, which can be important
# in some cases.
RqcdStat.r_qcd = r_qcd
RqcdSyst.r_qcd = r_qcd

# Set up patches
patch_definitions = {
    'is_electron': 'tau_0_truth_isEle',
    'is_muon': 'tau_0_truth_isMuon',
    'is_tau': 'tau_0_truth_isTau',
    'is_jet': 'tau_0_truth_isJet',
}

expr = partial(expression_substitute, definitions = patch_definitions)

tau_truth_matched = Patch(expr('[is_tau]'))
tau_fake = Patch(expr('![is_tau]'))
tau_electron_matched = Patch(expr('[is_electron]'))
tau_muon_matched = Patch(expr('[is_muon]'))
tau_lepton_matched = Patch(expr('[is_muon] || [is_electron]'))
tau_jet_fake = Patch(expr('!([is_muon] || [is_electron] || [is_tau])'))

# Create some utility functions
file = lambda name: join(data_prefix, name)

# Pileup-reweighting with PRWHash
# Friends are defined as (file, tree, index)
prw_friend = (file('prwTree.all.root'), 'prwTree', 'PRWHash')

# Create processes
data = Process(
    (
        # file('data.root'),
        file('hist-00276073.root'),
        file('hist-00276147.root'),
        file('hist-00276161.root'),
        file('hist-00276183.root'),
        file('hist-00276189.root'),
        file('hist-00276212.root'),
        file('hist-00276245.root'),
        file('hist-00276262.root'),
        file('hist-00276329.root'),
        file('hist-00276330.root'),
        file('hist-00276336.root'),
        file('hist-00276416.root'),
        file('hist-00276511.root'),
        file('hist-00276689.root'),
        file('hist-00276778.root'),
        file('hist-00276790.root'),
        file('hist-00276952.root'),
        file('hist-00276954.root'),
        file('hist-00278727.root'),
        file('hist-00278748.root'),
        file('hist-00278880.root'),
        file('hist-00278912.root'),
        file('hist-00278968.root'),
        file('hist-00278970.root'),
        file('hist-00279169.root'),
        file('hist-00279259.root'),
        file('hist-00279279.root'),
        file('hist-00279284.root'),
        file('hist-00279345.root'),
        file('hist-00279515.root'),
        file('hist-00279598.root'),
        file('hist-00279685.root'),
        file('hist-00279764.root'),
        file('hist-00279813.root'),
        file('hist-00279867.root'),
        file('hist-00279928.root'),
        file('hist-00279932.root'),
        file('hist-00279984.root'),
        file('hist-00280231.root'),
        file('hist-00280273.root'),
        file('hist-00280319.root'),
        file('hist-00280368.root'),
        file('hist-00280423.root'),
        file('hist-00280464.root'),
        file('hist-00280500.root'),
        file('hist-00280520.root'),
        file('hist-00280614.root'),
        file('hist-00280673.root'),
        file('hist-00280753.root'),
        file('hist-00280853.root'),
        file('hist-00280862.root'),
        file('hist-00280950.root'),
        file('hist-00280977.root'),
        file('hist-00281070.root'),
        file('hist-00281074.root'),
        file('hist-00281075.root'),
        file('hist-00281130.root'),
        file('hist-00281143.root'),
        file('hist-00281317.root'),
        file('hist-00281381.root'),
        file('hist-00281385.root'),
        file('hist-00281411.root'),
        file('hist-00282625.root'),
        file('hist-00282712.root'),
        file('hist-00282784.root'),
        file('hist-00282992.root'),
        file('hist-00283074.root'),
        file('hist-00283155.root'),
        file('hist-00283270.root'),
        file('hist-00283429.root'),
        file('hist-00283608.root'),
        file('hist-00283780.root'),
        file('hist-00284006.root'),
        file('hist-00284154.root'),
        file('hist-00284213.root'),
        file('hist-00284285.root'),
        file('hist-00284420.root'),
        file('hist-00284427.root'),
        file('hist-00284473.root'),
        file('hist-00284484.root'),
    ),
    tree = nominal_tree,
    label = 'Data',
    sample_type = 'data',
    line_color = 1,
    fill_color = 1,
    marker_style = 8,
)

ss_data = Process(
    (
        file('data.root'),
    ),
    tree = nominal_tree,
    label = 'SS Data',
    sample_type = 'data',
    line_color = 1,
    fill_color = 424,
    # metadata = {'print_me': ['estimation']},
)

zll = Process(
    (
        file('361106.root'),
        file('361107.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow ll',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 424,
)

ztautau = Process(
    (
        file('361108.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow#tau#tau',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 64,
)

wlnu = Process(
    (
        file('361100.root'),
        file('361101.root'),
        file('361103.root'),
        file('361104.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow l#nu',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 804,
)

wtaunu = Process(
    (
        file('361102.root'),
        file('361105.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow #tau#nu',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 806,
)

diboson = Process(
    (
        # PowhegPythia
        file('361600.root'),
        file('361601.root'),
        file('361602.root'),
        file('361603.root'),
        file('361604.root'),
        file('361605.root'),
        file('361606.root'),
        file('361607.root'),
        file('361608.root'),
        file('361609.root'),
        file('361610.root'),
        # Sherpa
        #file('361081.root'),
        #file('361082.root'),
        #file('361083.root'),
        #file('361084.root'),
        #file('361085.root'),
        #file('361086.root'),
        #file('361087.root'),
    ),
    tree = nominal_tree,
    label = 'Diboson',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 92,
)

single_top = Process(
    (
        file('410011.root'),
        file('410012.root'),
        file('410013.root'),
        file('410014.root'),
        #file('410025.root'),
        #file('410026.root'),
    ),
    tree = nominal_tree,
    label = 'Single Top',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 595,
)

single_top_true = single_top.patched(
    tau_truth_matched,
    label = 'Single Top (true #tau)',
    line_color = 1,
    fill_color = 920
)

single_top_lfake = single_top.patched(
    tau_lepton_matched,
    label = 'Single Top (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 865
)

single_top_jetfake = single_top.patched(
    tau_jet_fake,
    label = 'Single Top (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 411
)

ttbar = Process(
    (
        file('410000.root'),
        #file('410007.root'),
    ),
    tree = nominal_tree,
    label = 't#bar{t}',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 0,
)

ttbar_true = ttbar.patched(
    tau_truth_matched,
    label = 't#bar{t} (true #tau)',
    line_color = 1,
    fill_color = 0,
)

ttbar_lfake = ttbar.patched(
    tau_lepton_matched,
    label = 't#bar{t} (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 867,
)

ttbar_jetfake = ttbar.patched(
    tau_jet_fake,
    label = 't#bar{t} (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 406,
    # metadata = {'print_me': ['selection', 'expressions']},
    # metadata = {'print_me': ['estimation']},
)

# Other process for mu+tau
other = Process(
    zll.files() + \
        ztautau.files() + \
        wlnu.files() + \
        # diboson.files() + \
        wtaunu.files(),
    tree = nominal_tree,
    label = 'Other',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 92,
)

other_true = other.patched(
    tau_truth_matched,
    label = 'Other (true #tau)',
    line_color = 1,
    fill_color = 921
)

other_lfake = other.patched(
    tau_lepton_matched,
    label = 'Other (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 866
)

other_jetfake = other.patched(
    tau_jet_fake,
    label = 'Other (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 408
)

if systematics in ['Pruned', 'True']:
    mc_uncertainties = [
        #TestSystFlat,
        #TestSystShape,
        # Pruned MuonEffStat,
        # Pruned MuonEffSys,
        MuonEffTrigStat,
        MuonEffTrigSys,
        # Pruned MuonIsoStat,
        # Pruned MuonIsoSys,
        # Candidate MuonIdSys,
        # Candidate MuonMsSys,
        # Candidate MuonScaleSys,
        BJetEigenB0,
        BJetEigenB1,
        # Pruned BJetEigenB2,
        # Pruned BJetEigenB3,
        # Pruned BJetEigenB4,
        BJetEigenC0,
        # Pruned BJetEigenC1,
        # Pruned BJetEigenC2,
        # Pruned BJetEigenC3,
        BJetEigenLight0,
        # Pruned BJetEigenLight1,
        # Pruned BJetEigenLight2,
        # Pruned BJetEigenLight3,
        # Pruned BJetEigenLight4,
        # Pruned BJetEigenLight5,
        # Pruned BJetEigenLight6,
        # Pruned BJetEigenLight7,
        # Pruned BJetEigenLight8,
        # Pruned BJetEigenLight9,
        # Pruned BJetEigenLight10,
        # Pruned BJetEigenLight11,
        # Pruned BJetEigenLight12,
        # Pruned BJetEigenLight13,
        # Pruned BJetExtrapolation,
        #BJetExtrapolationCharm, # Doesn't work
    ]
    ss_data_uncertainties = [
        RqcdStat,
        RqcdSyst,
    ]
    osss_uncertainties = mc_uncertainties + ss_data_uncertainties

elif systematics == 'Full':
    mc_uncertainties = [
        #TestSystFlat,
        #TestSystShape,
        MuonEffStat,
        MuonEffSys,
        MuonEffTrigStat,
        MuonEffTrigSys,
        MuonIsoStat,
        MuonIsoSys,
        MuonIdSys,
        MuonMsSys,
        MuonScaleSys,
        BJetEigenB0,
        BJetEigenB1,
        BJetEigenB2,
        BJetEigenB3,
        BJetEigenB4,
        BJetEigenC0,
        BJetEigenC1,
        BJetEigenC2,
        BJetEigenC3,
        BJetEigenLight0,
        BJetEigenLight1,
        BJetEigenLight2,
        BJetEigenLight3,
        BJetEigenLight4,
        BJetEigenLight5,
        BJetEigenLight6,
        BJetEigenLight7,
        BJetEigenLight8,
        BJetEigenLight9,
        BJetEigenLight10,
        BJetEigenLight11,
        BJetEigenLight12,
        BJetEigenLight13,
        BJetExtrapolation,
        #BJetExtrapolationCharm, # Doesn't work
    ]
    ss_data_uncertainties = [
        RqcdStat,
        RqcdSyst,
    ]
    osss_uncertainties = mc_uncertainties + ss_data_uncertainties
else:
    mc_uncertainties = []
    ss_data_uncertainties = []
    osss_uncertainties = []

#mc_uncertainties = [
    #TestSystFlat,
    #TestSystShape,
#]

# Create models
mc = {
    'label': 'Data vs MC',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'backgrounds': OrderedDict((
        # ('diboson', {
            # 'process': diboson,
            # 'estimation': MonteCarlo,
            # 'uncertainties': mc_uncertainties,
        # }),
        ('wtaunu', {
            'process': wtaunu,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('zll', {
            'process': zll,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ztautau', {
            'process': ztautau,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('wlnu', {
            'process': wlnu,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top', {
            'process': single_top,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar', {
            'process': ttbar,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
    )),
}

mc_fakes = {
    'label': 'Data vs MC',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'backgrounds': OrderedDict((
        ('other_lfake', {
            'process': other_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_lepfake', {
            'process': single_top_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_lepfake', {
            'process': ttbar_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('other_jetfake', {
            'process': other_jetfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_jetfake', {
            'process': single_top_jetfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_jetfake', {
            'process': ttbar_jetfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('other_true', {
            'process': other_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_true', {
            'process': single_top_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
    )),
}

mc_sub = {
    'label': 'Data vs MC',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'backgrounds': OrderedDict((
        ('other_lfake', {
            'process': other_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_lepfake', {
            'process': single_top_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_lepfake', {
            'process': ttbar_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('other_jetfake', {
            'process': other_jetfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_jetfake', {
            'process': single_top_jetfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_jetfake', {
            'process': ttbar_jetfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
    )),
    'signals': OrderedDict((
        ('other_true', {
            'process': other_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_true', {
            'process': single_top_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
    )),
}
# Create OS-SS models
osss = {
    'label': 'OS-SS',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': OSData,
    },
    'backgrounds': OrderedDict((
        ('ss_data', {
            'process': ss_data,
            'estimation': SSData,
            'uncertainties': ss_data_uncertainties,
        }),
        ('zll', {
            'process': zll,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('ztautau', {
            'process': ztautau,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('wlnu', {
            'process': wlnu,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('wtaunu', {
            'process': wtaunu,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        # ('diboson', {
            # 'process': diboson,
            # 'estimation': OSSS,
            # 'uncertainties': mc_uncertainties,
        # }),
        ('single_top', {
            'process': single_top,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar', {
            'process': ttbar,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
    )),
}

osss_fakes = {
    'label': 'OS-SS',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': OSData,
    },
    'backgrounds': OrderedDict((
        ('ss_data', {
            'process': ss_data,
            'estimation': SSData,
            'uncertainties': ss_data_uncertainties,
        }),
        ('other_lfake', {
            'process': other_lfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('single_top_lfake', {
            'process': single_top_lfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('ttbar_lfake', {
            'process': ttbar_lfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('other_jetfake', {
            'process': other_jetfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('single_top_jetfake', {
            'process': single_top_jetfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('ttbar_jetfake', {
            'process': ttbar_jetfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('other_true', {
            'process': other_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
            'treat_as_signal': True,
        }),
        ('single_top_true', {
            'process': single_top_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
            'treat_as_signal': True,
        }),
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
            'treat_as_signal': True,
        }),
    )),
}

osss_sub = {
    'label': 'Bkg. Sub.',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'subtract_background': True,
    'data': {
        'process': data,
        'estimation': OSData,
    },
    'signals': OrderedDict((
        ('other_true', {
            'process': other_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('single_top_true', {
            'process': single_top_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
    )),
    'backgrounds': OrderedDict((
        ('ss_data', {
            'process': ss_data,
            'estimation': SSData,
            'uncertainties': ss_data_uncertainties,
        }),
        ('other_lfake', {
            'process': other_lfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('single_top_lfake', {
            'process': single_top_lfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('ttbar_lfake', {
            'process': ttbar_lfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('other_jetfake', {
            'process': other_jetfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('single_top_jetfake', {
            'process': single_top_jetfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('ttbar_jetfake', {
            'process': ttbar_jetfake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
    )),
}
