"""Standard data, and background models for the tau+jets analysis.
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

# owls-taunu imports
from owls_taunu.mutau.estimation import OSData, SSData, OSSS

# Load configuration
configuration = definitions()
enable_systematics = configuration.get('enable_systematics', '')
enable_systematics = True if enable_systematics == 'True' else False
data_prefix = configuration.get('data_prefix', '')
luminosity = float(configuration.get('luminosity', 1000.0)) # 1/fb
nominal_tree = 'NOMINAL'
sqrt_s = 13.0 * 1000 * 1000 # MeV


r_qcd = {
    'mu_tau': (1.2290379523389232, 0.03477053921717272),
    'mu_tau_qcd_cr': (1.2290379523389232, 0.03477053921717272),
    'mu_tau_qcd_cr_anti_tau': (1.0874001774622892, 0.011994208164661423),
    'mu_tau_qcd_cr_anti_tau_bveto': (1.2500163563325177, 0.006066506181587367)
}

MonteCarlo = partial(MonteCarlo, luminosity = luminosity)
OSSS = partial(OSSS, r_qcd = r_qcd, luminosity = luminosity)
SSData = partial(SSData, r_qcd = r_qcd)

# Set up patches
patch_definitions = {
    'is_had_tau': 'tau_0_matched_isHad',
    'is_electron': 'abs(tau_0_matched_pdgId) == 11',
    'is_muon': 'abs(tau_0_matched_pdgId) == 13',
    'is_tau': 'abs(tau_0_matched_pdgId) == 15',
    'is_b': 'abs(tau_0_matched_pdgId) == 5',
    'is_light': 'abs(tau_0_matched_pdgId) > 0 && abs(tau_0_matched_pdgId) < 5',
    'is_gluon': 'tau_0_matched_pdgId == 21',
    'is_isolated': (
        'lep_0_iso_ptcone40/lep_0_pt < 0.01 && '
        'lep_0_iso_etcone20/lep_0_pt < 0.04'),
}

expr = partial(expression_substitute, definitions = patch_definitions)

patch_definitions.update({
    'is_lepton': expr('[is_muon] || [is_electron]'),
    'is_not_jet': expr('[is_muon] || [is_electron] || [is_tau]'),
    'is_jet': expr('([is_light] || [is_b] || [is_gluon])'),
})

tau_truth_matched = Patch(expr('[is_had_tau] && [is_tau]'))
tau_fake = Patch(expr('[is_had_tau] && ![is_tau]'))
tau_electron_matched = Patch(expr('[is_had_tau] && [is_electron]'))
tau_muon_matched = Patch(expr('[is_had_tau] && [is_muon]'))
tau_lepton_matched = Patch(expr('[is_had_tau] && [is_lepton]'))
tau_jet_fake = Patch(expr('[is_had_tau] && [is_jet]'))
tau_non_jet_fake = Patch(expr('[is_not_jet]'))
tau_b_jet_fake = Patch(expr('[is_jet] && [is_b]'))
tau_light_jet_fake = Patch(expr('[is_jet] && [is_light]'))
tau_quark_jet_fake = Patch(expr('[is_jet] && ![is_gluon]'))
tau_gluon_jet_fake = Patch(expr('[is_jet] && [is_gluon]'))
isolated = Patch(expr('[is_isolated]'))
non_isolated = Patch(expr('![is_isolated]'))

# Create some utility functions
file = lambda name: join(data_prefix, name)

# Create processes
data = Process(
    (
        file('data.root'),
    ),
    tree = nominal_tree,
    label = 'Data',
    line_color = 1,
    fill_color = 1,
    marker_style = 8,
    metadata = {'sample_type': 'data'},
)

ss_data = Process(
    (
        file('data.root'),
    ),
    tree = nominal_tree,
    label = 'SS Data',
    line_color = 1,
    fill_color = 424,
    metadata = {'sample_type': 'data'},
)

zll = Process(
    (
        file('361106.root'),
        file('361107.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow ll',
    line_color = 1,
    fill_color = 424,
    metadata = {'sample_type': 'mc'},
)

ztautau = Process(
    (
        file('361108.root'),
    ),
    tree = nominal_tree,
    label = 'Z#rightarrow#tau#tau',
    line_color = 1,
    fill_color = 64,
    metadata = {'sample_type': 'mc'},
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
    line_color = 1,
    fill_color = 804,
    metadata = {'sample_type': 'mc'},
)

wtaunu = Process(
    (
        file('361102.root'),
        file('361105.root'),
    ),
    tree = nominal_tree,
    label = 'W#rightarrow #tau#nu',
    line_color = 1,
    fill_color = 806,
    metadata = {'sample_type': 'mc'},
)

diboson = Process(
    (
        # PowhegPythia
        #file('361600.root'),
        #file('361601.root'),
        #file('361602.root'),
        #file('361603.root'),
        #file('361604.root'),
        #file('361605.root'),
        #file('361606.root'),
        #file('361607.root'),
        #file('361608.root'),
        #file('361609.root'),
        #file('361610.root'),
        # Sherpa
        file('361081.root'),
        file('361082.root'),
        file('361083.root'),
        file('361084.root'),
        file('361085.root'),
        file('361086.root'),
        file('361087.root'),
    ),
    tree = nominal_tree,
    label = 'Diboson',
    line_color = 1,
    fill_color = 92,
    metadata = {'sample_type': 'mc'},
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
    line_color = 1,
    fill_color = 595,
    metadata = {'sample_type': 'mc'},
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

single_top_qfake = single_top.patched(
    tau_quark_jet_fake,
    label = 'Single Top (q #rightarrow #tau)',
    line_color = 1,
    fill_color = 411
)

single_top_gfake = single_top.patched(
    tau_gluon_jet_fake,
    label = 'Single Top (g #rightarrow #tau)',
    line_color = 1,
    fill_color = 805
)

ttbar = Process(
    (
        file('410000.root'),
        file('410007.root'),
    ),
    tree = nominal_tree,
    label = 't#bar{t}',
    line_color = 1,
    fill_color = 0,
    metadata = {'sample_type': 'mc'},
)

ttbar_true = ttbar.patched(
    tau_truth_matched,
    label = 't#bar{t} (true #tau)',
    line_color = 1,
    fill_color = 0
)

ttbar_fake = ttbar.patched(
    tau_fake,
    label = 't#bar{t} (fake #tau)',
    line_color = 1,
    fill_color = 406
)

ttbar_lfake = ttbar.patched(
    tau_lepton_matched,
    label = 't#bar{t} (l #rightarrow #tau)',
    line_color = 1,
    fill_color = 867
)

ttbar_efake = ttbar.patched(
    tau_electron_matched,
    label = 't#bar{t} (e #rightarrow #tau)',
    line_color = 1,
    fill_color = 424
)

ttbar_mufake = ttbar.patched(
    tau_muon_matched,
    label = 't#bar{t} (#mu #rightarrow #tau)',
    line_color = 1,
    fill_color = 609
)

ttbar_jetfake = ttbar.patched(
    tau_jet_fake,
    label = 't#bar{t} (j #rightarrow #tau)',
    line_color = 1,
    fill_color = 406
)

ttbar_qfake = ttbar.patched(
    tau_quark_jet_fake,
    label = 't#bar{t} (q #rightarrow #tau)',
    line_color = 1,
    fill_color = 406
)

ttbar_gfake = ttbar.patched(
    tau_gluon_jet_fake,
    label = 't#bar{t} (g #rightarrow #tau)',
    line_color = 1,
    fill_color = 807
)

# Other process for mu+tau
other = Process(
    zll.files() + \
        ztautau.files() + \
        wlnu.files() + \
        wtaunu.files() + \
        diboson.files(),
    tree = nominal_tree,
    label = 'Other',
    line_color = 1,
    fill_color = 92,
    metadata = {'sample_type': 'mc'},
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

other_qfake = other.patched(
    tau_quark_jet_fake,
    label = 'Other (q #rightarrow #tau)',
    line_color = 1,
    fill_color = 408
)

other_gfake = other.patched(
    tau_gluon_jet_fake,
    label = 'Other (g #rightarrow #tau)',
    line_color = 1,
    fill_color = 806
)


mc_uncertainties = []

# Create models
mc = {
    'label': 'MC vs data',
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
    'label': 'MC vs Data',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'backgrounds': OrderedDict((
        ('other_lepfake', {
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
    'label': 'MC vs Data',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'backgrounds': OrderedDict((
        ('other_lepfake', {
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
        ('other_gfake', {
            'process': other_gfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_gfake', {
            'process': single_top_gfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_gfake', {
            'process': ttbar_gfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('other_qfake', {
            'process': other_qfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_qfake', {
            'process': single_top_qfake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_qfake', {
            'process': ttbar_qfake,
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
    'label': 'MC vs Data (Bkg sub)',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': Plain,
    },
    'subtractions': dict((
        ('other', {
            'process': other,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top', {
            'process': single_top,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_fake', {
            'process': ttbar_fake,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
    )),
    'backgrounds': OrderedDict((
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': MonteCarlo,
            'uncertainties': mc_uncertainties,
        }),
    )),
}

ss_data_uncertainties = []
fakes_uncertainties = []

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

osss_sub = {
    'label': 'OS-SS (Bkg sub)',
    'luminosity': luminosity,
    'sqrt_s': sqrt_s,
    'data': {
        'process': data,
        'estimation': OSData,
    },
    'subtractions': dict((
        ('ss_data', {
            'process': ss_data,
            'estimation': SSData,
            'uncertainties': ss_data_uncertainties,
        }),
        ('other', {
            'process': other,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top', {
            'process': single_top,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_fake', {
            'process': ttbar_fake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
    )),
    'backgrounds': OrderedDict((
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': MonteCarlo,
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
        ('other_lepfake', {
            'process': other_lfake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_lfake', {
            'process': single_top_lfake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_lfake', {
            'process': ttbar_lfake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('other_jetfake', {
            'process': other_jetfake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_jetfake', {
            'process': single_top_jetfake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_jetfake', {
            'process': ttbar_jetfake,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('other_true', {
            'process': other_true,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('single_top_true', {
            'process': single_top_true,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
        ('ttbar_true', {
            'process': ttbar_true,
            'estimation': OSSS,
            'uncertainties': mc_uncertainties,
        }),
    )),
}
