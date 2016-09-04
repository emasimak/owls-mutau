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
import owls_mutau
from owls_mutau.estimation import OSData, SSData, OSSS
from owls_mutau.uncertainties import \
        TestConfiguration, TestSystFlat, TestSystShape, \
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

# NOTE: Remember to escape * to treat it like a multiplication sign in
# the regular expression
bjet_nominal = 'bjet_sf_MVX_NOMINAL_sf'
bjet_var = lambda v, d: 'bjet_sf_MVX_FT_EFF_Eigen_{0}_1{1}_sf'.format(v, d)
owls_mutau.uncertainties.configuration = {
    'NAME': '2015 MC15B',
    'MUON_EFF_STAT': (
        'lep_0_NOMINAL_effSF_RecoMedium',
        'lep_0_MUON_EFF_STAT_1up_effSF_RecoMedium',
        'lep_0_MUON_EFF_STAT_1down_effSF_RecoMedium'
    ),
    'MUON_EFF_SYS': (
        'lep_0_NOMINAL_effSF_RecoMedium',
        'lep_0_MUON_EFF_SYS_1up_effSF_RecoMedium',
        'lep_0_MUON_EFF_SYS_1down_effSF_RecoMedium'
    ),
    'MUON_EFF_TRIG_STAT': (
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
        'lep_0_MUON_EFF_TrigStatUncertainty_1up_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
        'lep_0_MUON_EFF_TrigStatUncertainty_1down_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'
    ),
    'MUON_EFF_TRIG_SYS': (
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
        'lep_0_MUON_EFF_TrigSystUncertainty_1up_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
        'lep_0_MUON_EFF_TrigSystUncertainty_1down_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'
    ),
    'MUON_ISO_STAT': (
        'lep_0_NOMINAL_effSF_IsoGradient',
        'lep_0_MUON_ISO_STAT_1up_effSF_IsoGradient',
        'lep_0_MUON_ISO_STAT_1down_effSF_IsoGradient'
    ),
    'MUON_ISO_SYS': (
        'lep_0_NOMINAL_effSF_IsoGradient',
        'lep_0_MUON_ISO_SYS_1up_effSF_IsoGradient',
        'lep_0_MUON_ISO_SYS_1down_effSF_IsoGradient'
    ),
    'MUON_ID_SYS': ('MUONS_ID_1up', 'MUONS_ID_1down'),
    'MUON_MS_SYS': ('MUONS_MS_1up', 'MUONS_MS_1down'),
    'MUON_SCALE_SYS': ('MUONS_SCALE_1up', 'MUONS_SCALE_1down'),
    'BJET_EIGEN_B0': (bjet_nominal, bjet_var('B_0', 'up'), bjet_var('B_0', 'down')),
    'BJET_EIGEN_B1': (bjet_nominal, bjet_var('B_1', 'up'), bjet_var('B_1', 'down')),
    'BJET_EIGEN_B2': (bjet_nominal, bjet_var('B_2', 'up'), bjet_var('B_2', 'down')),
    'BJET_EIGEN_B3': (bjet_nominal, bjet_var('B_3', 'up'), bjet_var('B_3', 'down')),
    'BJET_EIGEN_B4': (bjet_nominal, bjet_var('B_4', 'up'), bjet_var('B_4', 'down')),
    'BJET_EIGEN_C0': (bjet_nominal, bjet_var('C_0', 'up'), bjet_var('C_0', 'down')),
    'BJET_EIGEN_C1': (bjet_nominal, bjet_var('C_1', 'up'), bjet_var('C_1', 'down')),
    'BJET_EIGEN_C2': (bjet_nominal, bjet_var('C_2', 'up'), bjet_var('C_2', 'down')),
    'BJET_EIGEN_C3': (bjet_nominal, bjet_var('C_3', 'up'), bjet_var('C_3', 'down')),
    'BJET_EIGEN_LIGHT0': (bjet_nominal, bjet_var('Light_0', 'up'), bjet_var('Light_0', 'down')),
    'BJET_EIGEN_LIGHT1': (bjet_nominal, bjet_var('Light_1', 'up'), bjet_var('Light_1', 'down')),
    'BJET_EIGEN_LIGHT2': (bjet_nominal, bjet_var('Light_2', 'up'), bjet_var('Light_2', 'down')),
    'BJET_EIGEN_LIGHT3': (bjet_nominal, bjet_var('Light_3', 'up'), bjet_var('Light_3', 'down')),
    'BJET_EIGEN_LIGHT4': (bjet_nominal, bjet_var('Light_4', 'up'), bjet_var('Light_4', 'down')),
    'BJET_EIGEN_LIGHT5': (bjet_nominal, bjet_var('Light_5', 'up'), bjet_var('Light_5', 'down')),
    'BJET_EIGEN_LIGHT6': (bjet_nominal, bjet_var('Light_6', 'up'), bjet_var('Light_6', 'down')),
    'BJET_EIGEN_LIGHT7': (bjet_nominal, bjet_var('Light_7', 'up'), bjet_var('Light_7', 'down')),
    'BJET_EIGEN_LIGHT8': (bjet_nominal, bjet_var('Light_8', 'up'), bjet_var('Light_8', 'down')),
    'BJET_EIGEN_LIGHT9': (bjet_nominal, bjet_var('Light_9', 'up'), bjet_var('Light_9', 'down')),
    'BJET_EIGEN_LIGHT10': (bjet_nominal, bjet_var('Light_10', 'up'), bjet_var('Light_10', 'down')),
    'BJET_EIGEN_LIGHT11': (bjet_nominal, bjet_var('Light_11', 'up'), bjet_var('Light_11', 'down')),
    'BJET_EIGEN_LIGHT12': (bjet_nominal, bjet_var('Light_12', 'up'), bjet_var('Light_12', 'down')),
    'BJET_EIGEN_LIGHT13': (bjet_nominal, bjet_var('Light_13', 'up'), bjet_var('Light_13', 'down')),
    'BJET_EXTRAPOLATION': (bjet_nominal, 'bjet_sf_MVX_FT_EFF_extrapolation_1up_sf', 'bjet_sf_MVX_FT_EFF_extrapolation_1down_sf'),
    # 'BJET_EXTRAPOLATION_CHARM': (bjet_nominal, 'bjet_sf_MVX_FT_EFF_extrapolation from charm_1up_sf', 'bjet_sf_MVX_FT_EFF_extrapolation from charm_1down_sf'),
}

r_qcd = {
    'qcd_cr': [('tau_0_pt <= 40', 1.196, 0.019, 0.05), ('tau_0_pt > 40', 1.376, 0.041, 0.076)],
    'qcd_cr_1p': [('tau_0_pt <= 40', 1.185, 0.022, 0.055), ('tau_0_pt > 40', 1.284, 0.042, 0.081)],
    'qcd_cr_3p': [('tau_0_pt <= 35', 1.219, 0.041, 0.09), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.487, 0.088, 0.111), ('tau_0_pt > 50', 1.953, 0.223, 0.219)],
    'qcd_cr_loose': [('tau_0_pt <= 40', 1.15, 0.014, 0.026), ('tau_0_pt > 40', 1.303, 0.029, 0.049)],
    'qcd_cr_loose_1p': [('tau_0_pt <= 40', 1.133, 0.017, 0.037), ('tau_0_pt > 40', 1.236, 0.032, 0.052)],
    'qcd_cr_loose_3p': [('tau_0_pt <= 35', 1.167, 0.024, 0.049), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.324, 0.05, 0.098), ('tau_0_pt > 50', 1.578, 0.101, 0.078)],
    'qcd_cr_medium': [('tau_0_pt <= 40', 1.196, 0.019, 0.05), ('tau_0_pt > 40', 1.376, 0.041, 0.076)],
    'qcd_cr_medium_1p': [('tau_0_pt <= 40', 1.185, 0.022, 0.055), ('tau_0_pt > 40', 1.284, 0.042, 0.081)],
    'qcd_cr_medium_3p': [('tau_0_pt <= 35', 1.219, 0.041, 0.09), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.487, 0.088, 0.111), ('tau_0_pt > 50', 1.953, 0.223, 0.219)],
    'qcd_cr_tight': [('tau_0_pt <= 40', 1.238, 0.029, 0.076), ('tau_0_pt > 40', 1.355, 0.058, 0.079)],
    'qcd_cr_tight_1p': [('tau_0_pt <= 40', 1.198, 0.031, 0.08), ('tau_0_pt > 40', 1.28, 0.059, 0.097)],
    'qcd_cr_tight_3p': [('tau_0_pt <= 35', 1.389, 0.078, 0.197), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.702, 0.168, 0.191), ('tau_0_pt > 50', 1.828, 0.366, 0.423)],
    'qcd_cr_tau25': [('tau_0_pt <= 40', 1.222, 0.03, 0.099), ('tau_0_pt > 40', 1.429, 0.05, 0.098)],
    'qcd_cr_tau25_1p': [('tau_0_pt <= 40', 1.213, 0.031, 0.099), ('tau_0_pt > 40', 1.346, 0.052, 0.089)],
    'qcd_cr_tau25_3p': [('tau_0_pt <= 35', 1.222, 0.112, 0.186), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.578, 0.123, 0.17), ('tau_0_pt > 50', 2.06, 0.286, 0.329)],
    'qcd_cr_loose_tau25': [('tau_0_pt <= 40', 1.194, 0.023, 0.065), ('tau_0_pt > 40', 1.342, 0.036, 0.073)],
    'qcd_cr_loose_tau25_1p': [('tau_0_pt <= 40', 1.181, 0.025, 0.067), ('tau_0_pt > 40', 1.273, 0.039, 0.068)],
    'qcd_cr_loose_tau25_3p': [('tau_0_pt <= 35', 1.21, 0.076, 0.134), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.383, 0.073, 0.133), ('tau_0_pt > 50', 1.8, 0.154, 0.13)],
    'qcd_cr_medium_tau25': [('tau_0_pt <= 40', 1.222, 0.03, 0.099), ('tau_0_pt > 40', 1.429, 0.05, 0.098)],
    'qcd_cr_medium_tau25_1p': [('tau_0_pt <= 40', 1.213, 0.031, 0.099), ('tau_0_pt > 40', 1.346, 0.052, 0.089)],
    'qcd_cr_medium_tau25_3p': [('tau_0_pt <= 35', 1.222, 0.112, 0.186), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.578, 0.123, 0.17), ('tau_0_pt > 50', 2.06, 0.286, 0.329)],
    'qcd_cr_tight_tau25': [('tau_0_pt <= 40', 1.261, 0.042, 0.117), ('tau_0_pt > 40', 1.394, 0.069, 0.11)],
    'qcd_cr_tight_tau25_1p': [('tau_0_pt <= 40', 1.25, 0.044, 0.11), ('tau_0_pt > 40', 1.326, 0.07, 0.112)],
    'qcd_cr_tight_tau25_3p': [('tau_0_pt <= 35', 1.347, 0.187, 0.417), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.663, 0.209, 0.219), ('tau_0_pt > 50', 2.033, 0.48, 0.681)],
}

print('Using data 2015 with MC15B')
print('...and systematics configuration {}'.format((TestConfiguration())))

# Redefitions of estimations
MonteCarlo = partial(MonteCarlo, luminosity = luminosity)
OSSS = partial(OSSS, r_qcd = r_qcd, luminosity = luminosity)
SSData = partial(SSData, r_qcd = r_qcd)

# Set up patches
patch_definitions = {
    'is_electron': 'tau_0_truth_isEle',
    'is_muon': 'tau_0_truth_isMuon',
    'is_tau': 'tau_0_truth_isTau',
    'is_jet': 'tau_0_truth_isJet',
    'is_bjet': 'tau_0_truth_pdgId == 5',
}

expr = partial(expression_substitute, definitions = patch_definitions)

tau_truth_matched = Patch(expr('[is_tau]'))
tau_fake = Patch(expr('![is_tau]'))
tau_electron_matched = Patch(expr('[is_electron]'))
tau_muon_matched = Patch(expr('[is_muon]'))
tau_lepton_matched = Patch(expr('[is_muon] || [is_electron]'))
tau_jet_fake = Patch(expr('!([is_muon] || [is_electron] || [is_tau])'))
tau_bjet_fake = Patch(expr('[is_jet] && [is_bjet]'))
tau_lightjet_fake = Patch(expr('[is_jet] && ![is_bjet]'))

# Create some utility functions
file = lambda name: join(data_prefix, name)

# Pileup-reweighting with PRWHash
# Friends are defined as (file, tree, index)
prw_friend = (file('prwTree.all.root'), 'prwTree', 'PRWHash')

# Create processes
data = Process(
    (
        file('data.root'),
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
        data.files()
    ),
    tree = nominal_tree,
    label = 'MisID #tau (SS data)',
    sample_type = 'data',
    line_color = 1,
    fill_color = 410,
)

zll = Process(
    (
        file('361106.root'),
        file('361107.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow ll',
    sample_type = 'mc',
    friends = (prw_friend,),
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
    friends = (prw_friend,),
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
    friends = (prw_friend,),
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
    friends = (prw_friend,),
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
    friends = (prw_friend,),
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
    friends = (prw_friend,),
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
    friends = (prw_friend,),
    line_color = 1,
    fill_color = 0,
    # metadata = {'print_me': ['selection', 'expressions', 'counts']},
)

ttbar_true = ttbar.patched(
    tau_truth_matched,
    label = 't#bar{t} (true #tau)',
    line_color = 1,
    fill_color = 0,
    # metadata = {'print_me': ['selection', 'counts']},
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
    # metadata = {'print_me': ['syst', 'selection']},
    # metadata = {'print_me': ['estimation']},
)

ttbar_bjetfake = ttbar.patched(
        tau_bjet_fake,
        label = 't#bar{t} (b #rightarrow #tau)',
        line_color = 1,
        fill_color = 803
)

ttbar_lightjetfake = ttbar.patched(
        tau_lightjet_fake,
        label = 't#bar{t} (c,l,g #rightarrow #tau)',
        line_color = 1,
        fill_color = 406
)

# Other process for mu+tau
other = Process(
    zll.files() + \
        ztautau.files() + \
        wlnu.files() + \
        diboson.files() + \
        wtaunu.files(),
    tree = nominal_tree,
    label = 'Other',
    sample_type = 'mc',
    friends = (prw_friend,),
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

all_mc = Process(
    ttbar.files() + \
        single_top.files() + \
        zll.files() + \
        ztautau.files() + \
        wlnu.files() + \
        wtaunu.files(),
    tree = nominal_tree,
    label = 'All MC',
    sample_type = 'mc',
    friends = (prw_friend,),
    line_color = 1,
    fill_color = 92,
)

all_mc_true = all_mc.patched(
    tau_truth_matched,
    label = 'True #tau',
    line_color = 1,
    fill_color = 861,
    # metadata = {'print_me': ['selection', 'counts']},
)

all_mc_fake = all_mc.patched(
    tau_jet_fake,
    label = 'MisID #tau (MC)',
    line_color = 1,
    fill_color = 401,
    # metadata = {'print_me': ['selection', 'counts']},
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
        ('diboson', {
            'process': diboson,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
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

mc_fakes2 = {
    'label': 'Data vs MC',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'backgrounds': OrderedDict((
        ('all_mc_fake', {
            'process': all_mc_fake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('all_mc_true', {
            'process': all_mc_true,
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
        ('diboson', {
            'process': diboson,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
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
        ('all_mc_fake', {
            'process': all_mc_fake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
        ('all_mc_true', {
            'process': all_mc_true,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
            'treat_as_signal': True,
        }),
    )),
}

osss_fakes2 = {
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

osss_sub2 = {
    'label': 'Bkg. Sub.',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'subtract_background': True,
    'data': {
        'process': data,
        'estimation': OSData,
    },
    'signals': OrderedDict((
        ('all_mc_true', {
            'process': all_mc_true,
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
        ('all_mc_fake', {
            'process': all_mc_fake,
            'estimation': OSSS,
            'uncertainties': osss_uncertainties,
        }),
    )),
}
