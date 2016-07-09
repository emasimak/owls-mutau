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
year = configuration.get('year', '')

r_qcd_2015 = {
    'mu_tau_qcd_cr': [('tau_0_pt <= 40', 1.194, 0.014, 0.036), ('tau_0_pt > 40', 1.289, 0.025, 0.043)],
    'mu_tau_qcd_cr_1p': [('tau_0_pt <= 40', 1.171, 0.016, 0.041), ('tau_0_pt > 40', 1.241, 0.026, 0.059)],
    'mu_tau_qcd_cr_3p': [('tau_0_pt <= 35', 1.255, 0.031, 0.06), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.374, 0.058, 0.069), ('tau_0_pt > 50', 1.635, 0.114, 0.119)],
    'mu_tau_qcd_cr_loose_id': [('tau_0_pt <= 40', 1.158, 0.01, 0.028), ('tau_0_pt > 40', 1.258, 0.018, 0.034)],
    'mu_tau_qcd_cr_loose_id_1p': [('tau_0_pt <= 40', 1.141, 0.012, 0.033), ('tau_0_pt > 40', 1.209, 0.02, 0.044)],
    'mu_tau_qcd_cr_loose_id_3p': [('tau_0_pt <= 35', 1.18, 0.018, 0.039), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.288, 0.034, 0.055), ('tau_0_pt > 50', 1.45, 0.057, 0.067)],
    'mu_tau_qcd_cr_medium_id': [('tau_0_pt <= 40', 1.194, 0.014, 0.036), ('tau_0_pt > 40', 1.289, 0.025, 0.043)],
    'mu_tau_qcd_cr_medium_id_1p': [('tau_0_pt <= 40', 1.171, 0.016, 0.041), ('tau_0_pt > 40', 1.241, 0.026, 0.059)],
    'mu_tau_qcd_cr_medium_id_3p': [('tau_0_pt <= 35', 1.255, 0.031, 0.06), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.374, 0.058, 0.069), ('tau_0_pt > 50', 1.635, 0.114, 0.119)],
    'mu_tau_qcd_cr_tight_id': [('tau_0_pt <= 40', 1.231, 0.021, 0.059), ('tau_0_pt > 40', 1.324, 0.037, 0.055)],
    'mu_tau_qcd_cr_tight_id_1p': [('tau_0_pt <= 40', 1.193, 0.023, 0.062), ('tau_0_pt > 40', 1.284, 0.038, 0.061)],
    'mu_tau_qcd_cr_tight_id_3p': [('tau_0_pt <= 35', 1.362, 0.055, 0.108), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.595, 0.11, 0.084), ('tau_0_pt > 50', 1.536, 0.179, 0.178)],
    'mu_tau_qcd_cr_tau25': [('tau_0_pt <= 40', 1.225, 0.021, 0.04), ('tau_0_pt > 40', 1.304, 0.029, 0.048)],
    'mu_tau_qcd_cr_tau25_1p': [('tau_0_pt <= 40', 1.197, 0.022, 0.051), ('tau_0_pt > 40', 1.257, 0.031, 0.051)],
    'mu_tau_qcd_cr_tau25_3p': [('tau_0_pt <= 35', 1.468, 0.086, 0.132), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.428, 0.078, 0.078), ('tau_0_pt > 50', 1.661, 0.141, 0.108)],
    'mu_tau_qcd_cr_loose_id_tau25': [('tau_0_pt <= 40', 1.195, 0.016, 0.031), ('tau_0_pt > 40', 1.277, 0.022, 0.043)],
    'mu_tau_qcd_cr_loose_id_tau25_1p': [('tau_0_pt <= 40', 1.172, 0.018, 0.04), ('tau_0_pt > 40', 1.217, 0.024, 0.05)],
    'mu_tau_qcd_cr_loose_id_tau25_3p': [('tau_0_pt <= 35', 1.327, 0.052, 0.067), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.338, 0.049, 0.08), ('tau_0_pt > 50', 1.566, 0.081, 0.095)],
    'mu_tau_qcd_cr_medium_id_tau25': [('tau_0_pt <= 40', 1.225, 0.021, 0.04), ('tau_0_pt > 40', 1.304, 0.029, 0.048)],
    'mu_tau_qcd_cr_medium_id_tau25_1p': [('tau_0_pt <= 40', 1.197, 0.022, 0.051), ('tau_0_pt > 40', 1.257, 0.031, 0.051)],
    'mu_tau_qcd_cr_medium_id_tau25_3p': [('tau_0_pt <= 35', 1.468, 0.086, 0.132), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.428, 0.078, 0.078), ('tau_0_pt > 50', 1.661, 0.141, 0.108)],
    'mu_tau_qcd_cr_tight_id_tau25': [('tau_0_pt <= 40', 1.252, 0.029, 0.077), ('tau_0_pt > 40', 1.363, 0.043, 0.057)],
    'mu_tau_qcd_cr_tight_id_tau25_1p': [('tau_0_pt <= 40', 1.213, 0.03, 0.083), ('tau_0_pt > 40', 1.32, 0.045, 0.057)],
    'mu_tau_qcd_cr_tight_id_tau25_3p': [('tau_0_pt <= 35', 1.58, 0.144, 0.161), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.731, 0.149, 0.114), ('tau_0_pt > 50', 1.64, 0.226, 0.242)],
}

r_qcd_2016 = {
    'mu_tau_qcd_cr': [('tau_0_pt <= 40', 1.191, 0.016, 0.038), ('tau_0_pt > 40', 1.284, 0.025, 0.049)],
    'mu_tau_qcd_cr_1p': [('tau_0_pt <= 40', 1.164, 0.018, 0.032), ('tau_0_pt > 40', 1.243, 0.026, 0.041)],
    'mu_tau_qcd_cr_3p': [('tau_0_pt <= 35', 1.25, 0.036, 0.059), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.391, 0.064, 0.128), ('tau_0_pt > 50', 1.558, 0.102, 0.141)],
    'mu_tau_qcd_cr_loose_id': [('tau_0_pt <= 40', 1.166, 0.012, 0.024), ('tau_0_pt > 40', 1.268, 0.019, 0.04)],
    'mu_tau_qcd_cr_loose_id_1p': [('tau_0_pt <= 40', 1.154, 0.015, 0.021), ('tau_0_pt > 40', 1.223, 0.021, 0.03)],
    'mu_tau_qcd_cr_loose_id_3p': [('tau_0_pt <= 35', 1.18, 0.021, 0.043), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.305, 0.039, 0.104), ('tau_0_pt > 50', 1.413, 0.054, 0.08)],
    'mu_tau_qcd_cr_medium_id': [('tau_0_pt <= 40', 1.191, 0.016, 0.038), ('tau_0_pt > 40', 1.284, 0.025, 0.049)],
    'mu_tau_qcd_cr_medium_id_1p': [('tau_0_pt <= 40', 1.164, 0.018, 0.032), ('tau_0_pt > 40', 1.243, 0.026, 0.041)],
    'mu_tau_qcd_cr_medium_id_3p': [('tau_0_pt <= 35', 1.25, 0.036, 0.059), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.391, 0.064, 0.128), ('tau_0_pt > 50', 1.558, 0.102, 0.141)],
    'mu_tau_qcd_cr_tight_id': [('tau_0_pt <= 40', 1.218, 0.023, 0.058), ('tau_0_pt > 40', 1.331, 0.036, 0.047)],
    'mu_tau_qcd_cr_tight_id_1p': [('tau_0_pt <= 40', 1.195, 0.026, 0.05), ('tau_0_pt > 40', 1.281, 0.038, 0.061)],
    'mu_tau_qcd_cr_tight_id_3p': [('tau_0_pt <= 35', 1.284, 0.06, 0.115), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.556, 0.117, 0.182), ('tau_0_pt > 50', 1.68, 0.171, 0.175)],
    'mu_tau_qcd_cr_tau25': [('tau_0_pt <= 40', 1.176, 0.023, 0.078), ('tau_0_pt > 40', 1.325, 0.031, 0.063)],
    'mu_tau_qcd_cr_tau25_1p': [('tau_0_pt <= 40', 1.16, 0.024, 0.061), ('tau_0_pt > 40', 1.269, 0.032, 0.048)],
    'mu_tau_qcd_cr_tau25_3p': [('tau_0_pt <= 35', 1.228, 0.077, 0.237), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.543, 0.096, 0.192), ('tau_0_pt > 50', 1.612, 0.13, 0.215)],
    'mu_tau_qcd_cr_loose_id_tau25': [('tau_0_pt <= 40', 1.151, 0.018, 0.052), ('tau_0_pt > 40', 1.303, 0.024, 0.063)],
    'mu_tau_qcd_cr_loose_id_tau25_1p': [('tau_0_pt <= 40', 1.145, 0.02, 0.043), ('tau_0_pt > 40', 1.242, 0.026, 0.048)],
    'mu_tau_qcd_cr_loose_id_tau25_3p': [('tau_0_pt <= 35', 1.167, 0.051, 0.105), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.349, 0.059, 0.134), ('tau_0_pt > 50', 1.571, 0.082, 0.143)],
    'mu_tau_qcd_cr_medium_id_tau25': [('tau_0_pt <= 40', 1.176, 0.023, 0.078), ('tau_0_pt > 40', 1.325, 0.031, 0.063)],
    'mu_tau_qcd_cr_medium_id_tau25_1p': [('tau_0_pt <= 40', 1.16, 0.024, 0.061), ('tau_0_pt > 40', 1.269, 0.032, 0.048)],
    'mu_tau_qcd_cr_medium_id_tau25_3p': [('tau_0_pt <= 35', 1.228, 0.077, 0.237), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.543, 0.096, 0.192), ('tau_0_pt > 50', 1.612, 0.13, 0.215)],
    'mu_tau_qcd_cr_tight_id_tau25': [('tau_0_pt <= 40', 1.232, 0.032, 0.083), ('tau_0_pt > 40', 1.372, 0.044, 0.056)],
    'mu_tau_qcd_cr_tight_id_tau25_1p': [('tau_0_pt <= 40', 1.214, 0.033, 0.06), ('tau_0_pt > 40', 1.304, 0.045, 0.068)],
    'mu_tau_qcd_cr_tight_id_tau25_3p': [('tau_0_pt <= 35', 1.285, 0.118, 0.308), ('tau_0_pt > 35 && tau_0_pt <= 50', 1.802, 0.172, 0.256), ('tau_0_pt > 50', 1.83, 0.221, 0.24)],
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
    # friends = (prw_friend,),
    line_color = 1,
    fill_color = 92,
)

all_mc_true = all_mc.patched(
    tau_truth_matched,
    label = 'True #tau',
    line_color = 1,
    fill_color = 861
)

all_mc_fake = all_mc.patched(
    tau_fake,
    label = 'MisID #tau (MC)',
    line_color = 1,
    fill_color = 401
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
