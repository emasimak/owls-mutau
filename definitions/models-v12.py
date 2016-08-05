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
        TauIdSys, TauRecoSys, TauEleOlrSys, \
        RqcdStat, RqcdSyst, \
        PileupSys, \
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
year = configuration.get('year', '')

if year == '2015':
    trigger = 'HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoGradient'
elif year == '2016':
    trigger = 'HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoGradient'
else:
    raise RuntimeError('Don\'t know how to handle unknown year "{}.'. \
                       format(year))

# NOTE: Remember to escape * to treat it like a multiplication sign in
# the regular expression
bjet_nominal = 'jet_NOMINAL_global_effSF_MVX'
bjet_var = lambda v, d: 'jet_FT_EFF_Eigen_{0}_1{1}_global_effSF_MVX'.format(v, d)
owls_mutau.uncertainties.configuration = {
    'NAME': 'v12 {} {}'.format(year, trigger),
    'MUON_EFF_STAT': (
        'lep_0_NOMINAL_MuEffSF_Reco_QualMedium',
        'lep_0_MUON_EFF_STAT_1up_MuEffSF_Reco_QualMedium',
        'lep_0_MUON_EFF_STAT_1down_MuEffSF_Reco_QualMedium'
    ),
    'MUON_EFF_SYS': (
        'lep_0_NOMINAL_MuEffSF_Reco_QualMedium',
        'lep_0_MUON_EFF_SYS_1up_MuEffSF_Reco_QualMedium',
        'lep_0_MUON_EFF_SYS_1down_MuEffSF_Reco_QualMedium'
    ),
    'MUON_EFF_TRIG_STAT': (
        'lep_0_NOMINAL_MuEffSF_{}'.format(trigger),
        'lep_0_MUON_EFF_TrigStatUncertainty_1up_MuEffSF_{}'.format(trigger),
        'lep_0_MUON_EFF_TrigStatUncertainty_1down_MuEffSF_{}'.format(trigger),
    ),
    'MUON_EFF_TRIG_SYS': (
        'lep_0_NOMINAL_MuEffSF_{}'.format(trigger),
        'lep_0_MUON_EFF_TrigSystUncertainty_1up_MuEffSF_{}'.format(trigger),
        'lep_0_MUON_EFF_TrigSystUncertainty_1down_MuEffSF_{}'.format(trigger),
    ),
    'MUON_ISO_STAT': (
        'lep_0_NOMINAL_MuEffSF_IsoGradient',
        'lep_0_MUON_ISO_STAT_1up_MuEffSF_IsoGradient',
        'lep_0_MUON_ISO_STAT_1down_MuEffSF_IsoGradient',
    ),
    'MUON_ISO_SYS': (
        'lep_0_NOMINAL_MuEffSF_IsoGradient',
        'lep_0_MUON_ISO_STAT_1up_MuEffSF_IsoGradient',
        'lep_0_MUON_ISO_STAT_1down_MuEffSF_IsoGradient',
    ),
    'MUON_ID_SYS': ('MUONS_ID_1up', 'MUONS_ID_1down'),
    'MUON_MS_SYS': ('MUONS_MS_1up', 'MUONS_MS_1down'),
    'MUON_SCALE_SYS': ('MUONS_SCALE_1up', 'MUONS_SCALE_1down'),
    'TAU_ID_SYS': (
        'tau_0_NOMINAL_TauEffSF_JetBDT(loose|medium|tight)',
        'tau_0_TAUS_TRUEHADTAU_EFF_JETID_TOTAL_1up_TauEffSF_JetBDT\\1',
        'tau_0_TAUS_TRUEHADTAU_EFF_JETID_TOTAL_1down_TauEffSF_JetBDT\\1'
    ),
    'TAU_RECO_SYS': (
        'tau_0_NOMINAL_TauEffSF_reco',
        'tau_0_TAUS_TRUEHADTAU_EFF_RECO_TOTAL_1up_TauEffSF_reco',
        'tau_0_TAUS_TRUEHADTAU_EFF_RECO_TOTAL_1down_TauEffSF_reco'
    ),
    'TAU_ELEOLR_SYS': (
        'tau_0_NOMINAL_TauEffSF_HadTauEleOLR_tauhad',
        'tau_0_TAUS_TRUEHADTAU_EFF_ELEOLR_TOTAL_1up_TauEffSF_HadTauEleOLR_tauhad',
        'tau_0_TAUS_TRUEHADTAU_EFF_ELEOLR_TOTAL_1down_TauEffSF_HadTauEleOLR_tauhad'
    ),
    'PRW_SYS': (
        'NOMINAL_pileup_combined_weight',
        'PRW_DATASF_1up_pileup_combined_weight',
        'PRW_DATASF_1down_pileup_combined_weight'
    ),
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
    'BJET_EXTRAPOLATION': (bjet_nominal, 'jet_FT_EFF_extrapolation_1up_global_effSF_MVX', 'jet_FT_EFF_extrapolation_1up_global_effSF_MVX'),
    'BJET_EXTRAPOLATION_CHARM': (bjet_nominal, 'jet_FT_EFF_extrapolation_from_charm_1up_global_effSF_MVX', 'jet_FT_EFF_extrapolation_from_charm_1down_global_effSF_MVX'),
}

r_qcd_2015 = {
    'qcd_cr': [('tau_0_pt <= 40', 1.188, 0.014, 0.035), ('tau_0_pt > 40', 1.279, 0.025, 0.042)],
    'qcd_cr_1p': [('tau_0_pt <= 40', 1.163, 0.016, 0.04), ('tau_0_pt > 40', 1.231, 0.026, 0.058)],
    'qcd_cr_3p': [('tau_0_pt <= 35', 1.252, 0.031, 0.06), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.361, 0.057, 0.071), ('tau_0_pt > 50', 1.623, 0.113, 0.117)],
    'qcd_cr_loose_id': [('tau_0_pt <= 40', 1.153, 0.01, 0.027), ('tau_0_pt > 40', 1.251, 0.018, 0.033)],
    'qcd_cr_loose_id_1p': [('tau_0_pt <= 40', 1.135, 0.012, 0.032), ('tau_0_pt > 40', 1.202, 0.02, 0.043)],
    'qcd_cr_loose_id_3p': [('tau_0_pt <= 35', 1.178, 0.018, 0.039), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.281, 0.034, 0.055), ('tau_0_pt > 50', 1.442, 0.056, 0.066)],
    'qcd_cr_medium_id': [('tau_0_pt <= 40', 1.188, 0.014, 0.035), ('tau_0_pt > 40', 1.279, 0.025, 0.042)],
    'qcd_cr_medium_id_1p': [('tau_0_pt <= 40', 1.163, 0.016, 0.04), ('tau_0_pt > 40', 1.231, 0.026, 0.058)],
    'qcd_cr_medium_id_3p': [('tau_0_pt <= 35', 1.252, 0.031, 0.06), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.361, 0.057, 0.071), ('tau_0_pt > 50', 1.623, 0.113, 0.117)],
    'qcd_cr_tight_id': [('tau_0_pt <= 40', 1.222, 0.021, 0.059), ('tau_0_pt > 40', 1.312, 0.036, 0.054)],
    'qcd_cr_tight_id_1p': [('tau_0_pt <= 40', 1.183, 0.023, 0.062), ('tau_0_pt > 40', 1.273, 0.038, 0.06)],
    'qcd_cr_tight_id_3p': [('tau_0_pt <= 35', 1.357, 0.055, 0.11), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.587, 0.11, 0.088), ('tau_0_pt > 50', 1.513, 0.178, 0.172)],
    'qcd_cr_tau25': [('tau_0_pt <= 40', 1.214, 0.021, 0.041), ('tau_0_pt > 40', 1.291, 0.029, 0.046)],
    'qcd_cr_tau25_1p': [('tau_0_pt <= 40', 1.186, 0.022, 0.05), ('tau_0_pt > 40', 1.245, 0.031, 0.049)],
    'qcd_cr_tau25_3p': [('tau_0_pt <= 35', 1.457, 0.086, 0.135), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.411, 0.078, 0.078), ('tau_0_pt > 50', 1.65, 0.141, 0.108)],
    'qcd_cr_loose_id_tau25': [('tau_0_pt <= 40', 1.187, 0.016, 0.032), ('tau_0_pt > 40', 1.267, 0.022, 0.043)],
    'qcd_cr_loose_id_tau25_1p': [('tau_0_pt <= 40', 1.163, 0.018, 0.04), ('tau_0_pt > 40', 1.208, 0.024, 0.049)],
    'qcd_cr_loose_id_tau25_3p': [('tau_0_pt <= 35', 1.323, 0.052, 0.069), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.329, 0.049, 0.08), ('tau_0_pt > 50', 1.557, 0.081, 0.093)],
    'qcd_cr_medium_id_tau25': [('tau_0_pt <= 40', 1.214, 0.021, 0.041), ('tau_0_pt > 40', 1.291, 0.029, 0.046)],
    'qcd_cr_medium_id_tau25_1p': [('tau_0_pt <= 40', 1.186, 0.022, 0.05), ('tau_0_pt > 40', 1.245, 0.031, 0.049)],
    'qcd_cr_medium_id_tau25_3p': [('tau_0_pt <= 35', 1.457, 0.086, 0.135), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.411, 0.078, 0.078), ('tau_0_pt > 50', 1.65, 0.141, 0.108)],
    'qcd_cr_tight_id_tau25': [('tau_0_pt <= 40', 1.236, 0.029, 0.08), ('tau_0_pt > 40', 1.347, 0.043, 0.054)],
    'qcd_cr_tight_id_tau25_1p': [('tau_0_pt <= 40', 1.198, 0.03, 0.085), ('tau_0_pt > 40', 1.305, 0.045, 0.056)],
    'qcd_cr_tight_id_tau25_3p': [('tau_0_pt <= 35', 1.55, 0.142, 0.171), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.714, 0.148, 0.116), ('tau_0_pt > 50', 1.624, 0.225, 0.25)],
}

r_qcd_2016 = {
    'qcd_cr': [('tau_0_pt <= 40', 1.153, 0.029, 0.036), ('tau_0_pt > 40', 1.189, 0.041, 0.076)],
    'qcd_cr_1p': [('tau_0_pt <= 40', 1.121, 0.033, 0.055), ('tau_0_pt > 40', 1.187, 0.045, 0.093)],
    'qcd_cr_3p': [('tau_0_pt <= 35', 1.244, 0.068, 0.202), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.243, 0.109, 0.149), ('tau_0_pt > 50', 1.208, 0.127, 0.217)],
    'qcd_cr_tau60': [('', 1.206, 0.063, 0.08)],
    'qcd_cr_tau60_1p': [('', 1.191, 0.068, 0.099)],
    'qcd_cr_tau60_3p': [('', 1.286, 0.166, 0.211)],
    'qcd_cr_loose_id': [('tau_0_pt <= 40', 1.103, 0.021, 0.032), ('tau_0_pt > 40', 1.17, 0.031, 0.036)],
    'qcd_cr_loose_id_1p': [('tau_0_pt <= 40', 1.092, 0.026, 0.067), ('tau_0_pt > 40', 1.146, 0.036, 0.043)],
    'qcd_cr_loose_id_3p': [('tau_0_pt <= 35', 1.141, 0.039, 0.105), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.103, 0.063, 0.113), ('tau_0_pt > 50', 1.284, 0.085, 0.215)],
    'qcd_cr_medium_id': [('tau_0_pt <= 40', 1.153, 0.029, 0.036), ('tau_0_pt > 40', 1.189, 0.041, 0.076)],
    'qcd_cr_medium_id_1p': [('tau_0_pt <= 40', 1.121, 0.033, 0.055), ('tau_0_pt > 40', 1.187, 0.045, 0.093)],
    'qcd_cr_medium_id_3p': [('tau_0_pt <= 35', 1.244, 0.068, 0.202), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.243, 0.109, 0.149), ('tau_0_pt > 50', 1.208, 0.127, 0.217)],
    'qcd_cr_tight_id': [('tau_0_pt <= 40', 1.209, 0.043, 0.077), ('tau_0_pt > 40', 1.259, 0.06, 0.141)],
    'qcd_cr_tight_id_1p': [('tau_0_pt <= 40', 1.165, 0.046, 0.116), ('tau_0_pt > 40', 1.2, 0.062, 0.154)],
    'qcd_cr_tight_id_3p': [('tau_0_pt <= 35', 1.402, 0.127, 0.224), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.701, 0.248, 0.224), ('tau_0_pt > 50', 1.494, 0.23, 0.289)],
    'qcd_cr_tau25': [('tau_0_pt <= 40', 1.161, 0.041, 0.063), ('tau_0_pt > 40', 1.183, 0.048, 0.114)],
    'qcd_cr_tau25_1p': [('tau_0_pt <= 40', 1.134, 0.044, 0.036), ('tau_0_pt > 40', 1.172, 0.052, 0.15)],
    'qcd_cr_tau25_3p': [('tau_0_pt <= 35', 1.389, 0.168, 0.346), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.287, 0.146, 0.191), ('tau_0_pt > 50', 1.2, 0.15, 0.359)],
    'qcd_cr_tau60_tau25': [('', 1.183, 0.074, 0.097)],
    'qcd_cr_tau60_tau25_1p': [('', 1.171, 0.08, 0.1)],
    'qcd_cr_tau60_tau25_3p': [('', 1.246, 0.196, 0.307)],
    'qcd_cr_loose_id_tau25': [('tau_0_pt <= 40', 1.115, 0.033, 0.051), ('tau_0_pt > 40', 1.164, 0.039, 0.047)],
    'qcd_cr_loose_id_tau25_1p': [('tau_0_pt <= 40', 1.122, 0.037, 0.036), ('tau_0_pt > 40', 1.123, 0.042, 0.061)],
    'qcd_cr_loose_id_tau25_3p': [('tau_0_pt <= 35', 1.164, 0.099, 0.242), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.139, 0.092, 0.121), ('tau_0_pt > 50', 1.297, 0.115, 0.218)],
    'qcd_cr_medium_id_tau25': [('tau_0_pt <= 40', 1.161, 0.041, 0.063), ('tau_0_pt > 40', 1.183, 0.048, 0.114)],
    'qcd_cr_medium_id_tau25_1p': [('tau_0_pt <= 40', 1.134, 0.044, 0.036), ('tau_0_pt > 40', 1.172, 0.052, 0.15)],
    'qcd_cr_medium_id_tau25_3p': [('tau_0_pt <= 35', 1.389, 0.168, 0.346), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.287, 0.146, 0.191), ('tau_0_pt > 50', 1.2, 0.15, 0.359)],
    'qcd_cr_tight_id_tau25': [('tau_0_pt <= 40', 1.244, 0.059, 0.051), ('tau_0_pt > 40', 1.321, 0.073, 0.18)],
    'qcd_cr_tight_id_tau25_1p': [('tau_0_pt <= 40', 1.201, 0.06, 0.087), ('tau_0_pt > 40', 1.247, 0.074, 0.197)],
    'qcd_cr_tight_id_tau25_3p': [('tau_0_pt <= 35', 1.673, 0.307, 0.568), ('tau_0_pt > 35 && tau_0_pt <= 50', 2.016, 0.369, 0.384), ('tau_0_pt > 50', 1.661, 0.302, 0.222)],
}

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
data_2015 = Process(
    (

        file('00276262.root'),
        file('00276329.root'),
        file('00276330.root'),
        file('00276336.root'),
        file('00276416.root'),
        file('00276511.root'),
        file('00276689.root'),
        file('00276731.root'),
        file('00276778.root'),
        file('00276790.root'),
        file('00276952.root'),
        file('00276954.root'),
        file('00278727.root'),
        file('00278748.root'),
        file('00278880.root'),
        file('00278912.root'),
        file('00278968.root'),
        file('00278970.root'),
        file('00279169.root'),
        file('00279259.root'),
        file('00279279.root'),
        file('00279284.root'),
        file('00279345.root'),
        file('00279515.root'),
        file('00279598.root'),
        file('00279685.root'),
        file('00279764.root'),
        file('00279813.root'),
        file('00279867.root'),
        file('00279928.root'),
        file('00279932.root'),
        file('00279984.root'),
        file('00280231.root'),
        file('00280273.root'),
        file('00280319.root'),
        file('00280368.root'),
        file('00280423.root'),
        file('00280464.root'),
        file('00280500.root'),
        file('00280520.root'),
        file('00280614.root'),
        file('00280673.root'),
        file('00280753.root'),
        file('00280853.root'),
        file('00280862.root'),
        file('00280950.root'),
        file('00280977.root'),
        file('00281070.root'),
        file('00281074.root'),
        file('00281075.root'),
        file('00281130.root'),
        file('00281143.root'),
        file('00281317.root'),
        file('00281381.root'),
        file('00281385.root'),
        file('00281411.root'),
        file('00282625.root'),
        file('00282631.root'),
        file('00282712.root'),
        file('00282784.root'),
        file('00282992.root'),
        file('00283074.root'),
        file('00283155.root'),
        file('00283270.root'),
        file('00283429.root'),
        file('00283608.root'),
        file('00283780.root'),
        file('00284006.root'),
        file('00284154.root'),
        file('00284213.root'),
        file('00284285.root'),
        file('00284420.root'),
        file('00284427.root'),
        file('00284473.root'),
        file('00284484.root'),

    ),
    tree = nominal_tree,
    label = 'Data 2015',
    sample_type = 'data',
    line_color = 1,
    fill_color = 1,
    marker_style = 8,
    # metadata = {'print_me': ['counts', 'selection']},
)

data_2016 = Process(
    (

        file('00297730.root'),
        file('00298591.root'),
        file('00298595.root'),
        file('00298609.root'),
        file('00298633.root'),
        file('00298687.root'),
        file('00298690.root'),
        file('00298771.root'),
        file('00298773.root'),
        file('00298862.root'),
        file('00298967.root'),
        file('00299055.root'),
        file('00299144.root'),
        file('00299147.root'),
        file('00299184.root'),
        file('00299241.root'),
        file('00299243.root'),
        file('00299288.root'),
        file('00299315.root'),
        file('00299340.root'),
        file('00299343.root'),
        file('00299390.root'),
        file('00299584.root'),
        file('00300279.root'),
        file('00300287.root'),
        file('00300345.root'),
        file('00300415.root'),
        file('00300418.root'),
        file('00300487.root'),
        file('00300540.root'),
        file('00300571.root'),
        file('00300600.root'),
        file('00300655.root'),
        file('00300687.root'),
        file('00300784.root'),
        file('00300800.root'),
        file('00300863.root'),
        file('00300908.root'),
        file('00301912.root'),
        file('00301915.root'),
        file('00301918.root'),
        file('00301932.root'),
        file('00301973.root'),
        file('00302053.root'),
        file('00302137.root'),
        file('00302265.root'),
        file('00302269.root'),
        file('00302300.root'),
        file('00302347.root'),
        file('00302380.root'),
        file('00302391.root'),
        file('00302393.root'),
        file('00302737.root'),
        file('00302829.root'),
        file('00302831.root'),
        file('00302872.root'),
        file('00302919.root'),
        file('00302925.root'),
        file('00302956.root'),
        file('00303007.root'),
        file('00303059.root'),
        file('00303079.root'),
        file('00303201.root'),
        file('00303208.root'),
        file('00303264.root'),
        file('00303266.root'),
        file('00303291.root'),

    ),
    tree = nominal_tree,
    label = 'Data 2016',
    sample_type = 'data',
    line_color = 1,
    fill_color = 1,
    marker_style = 8,
)

zll_2015 = Process(
    (
        file('361106.2015.root'),
        file('361107.2015.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow ll',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 424,
)

zll_2016 = Process(
    (
        file('361106.2016.root'),
        file('361107.2016.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow ll',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 424,
)

ztautau_2015 = Process(
    (
        file('361108.2015.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow#tau#tau',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 64,
)

ztautau_2016 = Process(
    (
        file('361108.2016.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow#tau#tau',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 64,
)

wlnu_2015 = Process(
    (
        file('361100.2015.root'),
        file('361101.2015.root'),
        file('361103.2015.root'),
        file('361104.2015.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow l#nu',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 804,
)

wlnu_2016 = Process(
    (
        file('361100.2016.root'),
        file('361101.2016.root'),
        file('361103.2016.root'),
        file('361104.2016.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow l#nu',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 804,
)

wtaunu_2015 = Process(
    (
        file('361102.2015.root'),
        file('361105.2015.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow #tau#nu',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 806,
)

wtaunu_2016 = Process(
    (
        file('361102.2016.root'),
        file('361105.2016.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow #tau#nu',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 806,
)

single_top_2015 = Process(
    (
        file('410011.2015.root'),
        file('410012.2015.root'),
        file('410013.2015.root'),
        file('410014.2015.root'),
        file('410025.2015.root'),
        # file('410026.2015.root'),
    ),
    tree = nominal_tree,
    label = 'Single Top',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 595,
)

single_top_2016 = Process(
    (
        file('410011.2016.root'),
        file('410012.2016.root'),
        file('410013.2016.root'),
        file('410014.2016.root'),
        file('410025.2016.root'),
        file('410026.2016.root'),
    ),
    tree = nominal_tree,
    label = 'Single Top',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 595,
)

ttbar_2015 = Process(
    (
        file('410000.2015.part_1.root'),
        file('410000.2015.part_2.root'),
    ),
    tree = nominal_tree,
    label = 't#bar{t}',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 0,
    # metadata = {'print_me': ['expression', 'selection', 'counts']},
    # metadata = {'print_me': ['counts']},
)

ttbar_2016 = Process(
    (
        file('410000.2016.root'),
    ),
    tree = nominal_tree,
    label = 't#bar{t}',
    sample_type = 'mc',
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 0,
)


if year == '2015':
    data = data_2015
    zll = zll_2015
    ztautau = ztautau_2015
    wlnu = wlnu_2015
    wtaunu = wtaunu_2015
    single_top = single_top_2015
    ttbar = ttbar_2015
    r_qcd = r_qcd_2015
elif year == '2016':
    data = data_2016
    zll = zll_2016
    ztautau = ztautau_2016
    wlnu = wlnu_2016
    wtaunu = wtaunu_2016
    single_top = single_top_2016
    ttbar = ttbar_2016
    r_qcd = r_qcd_2016
else:
    raise RuntimeError('Don\'t know how to handle unknown year "{}.'. \
                       format(year))
print('Using data {} with year {}'.format(data.label(), year))
print('...and systematics configuration {}'.format((TestConfiguration())))


# Redefitions of estimations
MonteCarlo = partial(MonteCarlo, luminosity = luminosity)
OSSS = partial(OSSS, r_qcd = r_qcd, luminosity = luminosity)
SSData = partial(SSData, r_qcd = r_qcd)

# Redefitions of uncertainties
# NOTE: This is a cleaner way to initialize the class with an rQCD value than
# invoking partial. When invoking partial, the type of the class is exchanged
# with the partial type. This prevents class comparison, which can be important
# in some cases.
# RqcdStat.r_qcd = r_qcd
# RqcdSyst.r_qcd = r_qcd

ss_data = Process(
    (
        data.files()
    ),
    tree = nominal_tree,
    label = 'MisID #tau (SS data)',
    sample_type = 'data',
    line_color = 1,
    fill_color = 410,
    # metadata = {'print_me': ['estimation']},
)

single_top_true = single_top.patched(
    tau_truth_matched,
    label = 'Single Top (true #tau)',
    line_color = 1,
    fill_color = 920,
    # metadata = {'print_me': ['estimation']},
)

single_top_lfake = single_top.patched(
    tau_lepton_matched,
    label = 'Single Top (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 865,
    # metadata = {'print_me': ['estimation']},
)

single_top_jetfake = single_top.patched(
    tau_jet_fake,
    label = 'Single Top (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 411,
    # metadata = {'print_me': ['estimation']},
)

ttbar_true = ttbar.patched(
    tau_truth_matched,
    label = 't#bar{t} (true #tau)',
    line_color = 1,
    fill_color = 0,
    # metadata = {'print_me': ['counts']},
    # metadata = {'print_me': ['estimation', 'selection', 'counts']},
    # metadata = {'print_me': ['selection', 'counts']},
)

ttbar_lfake = ttbar.patched(
    tau_lepton_matched,
    label = 't#bar{t} (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 867,
    # metadata = {'print_me': ['counts']},
    # metadata = {'print_me': ['estimation']},
)

ttbar_jetfake = ttbar.patched(
    tau_jet_fake,
    label = 't#bar{t} (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 406,
    # metadata = {'print_me': ['counts']},
    # metadata = {'print_me': ['estimation']},
)

# Other process for mu+tau
other = Process(
    zll.files() + \
        ztautau.files() + \
        wlnu.files() + \
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
    fill_color = 921,
    # metadata = {'print_me': ['estimation']},
)

other_lfake = other.patched(
    tau_lepton_matched,
    label = 'Other (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 866,
    # metadata = {'print_me': ['estimation']},
)

other_jetfake = other.patched(
    tau_jet_fake,
    label = 'Other (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 408,
    # metadata = {'print_me': ['estimation']},
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
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 92,
)

all_mc_true = all_mc.patched(
    tau_truth_matched,
    label = 'True #tau',
    line_color = 1,
    fill_color = 861,
    # metadata = {'print_me': ['counts']},
)

all_mc_fake = all_mc.patched(
    tau_fake,
    label = 'MisID #tau (MC)',
    line_color = 1,
    fill_color = 401,
    # metadata = {'print_me': ['counts']},
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
        TauIdSys,
        TauRecoSys,
        TauEleOlrSys,
        PileupSys,
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
        # Pruuned BJetExtrapolationCharm,
    ]
    ss_data_uncertainties = [
        RqcdStat,
        RqcdSyst,
    ]
    osss_uncertainties = mc_uncertainties + ss_data_uncertainties
elif systematics == 'Efficiency':
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
        # Candidate TauIdSys,
        # Candidate TauRecoSys,
        # Candidate TauEleOlrSys,
        PileupSys,
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
        TauIdSys,
        # TauRecoSys,
        # TauEleOlrSys,
        PileupSys,
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
        ('single_top_lfake', {
            'process': single_top_lfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_lfake', {
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
