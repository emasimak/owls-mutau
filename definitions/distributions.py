"""Plots for the mu+tau analysis.
"""

# TODO: Split this file into several

# owls-hep imports
from owls_hep.histogramming import Histogram
from owls_hep.efficiency import Efficiency

tau_pt = Histogram(
        'tau_0_pt',
        (20, 0, 200),
        '',
        '#tau p_{T} [GeV]',
        'Events / 10 GeV'
        )

tau_pt_b1 = Histogram(
        'tau_0_pt',
        (15, 0, 300),
        '',
        '#tau p_{T} [GeV]',
        'Events / 20 GeV'
        )

tau_pt_b2 = Histogram(
        'tau_0_pt',
        (10, 50, 150),
        '',
        '#tau p_{T} [GeV]',
        'Events / 10 GeV'
        )

tau_eta = Histogram(
        'tau_0_eta',
        (20, -3.0, 3.0),
        '',
        '#tau #eta',
        'Events'
        )

tau_phi = Histogram(
        'tau_0_phi',
        (16, -3.2, 3.2),
        '',
        '#tau #phi',
        'Events'
        )

# Tau ID variables
tau_bdt_score = Histogram(
        'tau_0_jet_bdt_score',
        (20, 0.5, 1.5),
        '',
        '#tau BDT score',
        'Events'
        )

tau_n_tracks = Histogram(
        'tau_0_n_tracks',
        (11, -0.5, 10.5),
        '',
        '#tau N_{track}',
        'Events'
        )

tau_n_trk_core_wide = Histogram(
        'tau_0_trk_multi_cws_dr60_d04_n_lp5',
        (11, -0.5, 10.5),
        '',
        'tau_0_trk_multi_cws_dr60_d04_n_lp5',
        #'N_{core+wide}',
        'Events'
        )

# Tau trigger variables
tau_hlt_pt = Histogram(
        'tau_0_HLT_pt',
        (15, 0, 300),
        '',
        'HLT #tau p_{T} [GeV]',
        'Events / 20 GeV'
        )

tau_hlt_eta = Histogram(
        'tau_0_hlt_eta',
        (20, -3.0, 3.0),
        '',
        'HLT #tau #eta',
        'Events'
        )

tau_hlt_phi = Histogram(
        'tau_0_HLT_phi',
        (16, -3.2, 3.2),
        '',
        'HLT #tau #phi',
        'Events'
        )

mu_pt = Histogram(
        'lep_0_pt',
        (20, 0, 200),
        '',
        '#mu p_{T} [GeV]',
        'Events / 10 GeV'
        )

mu_eta = Histogram(
        'lep_0_eta',
        (20, -3.0, 3.0),
        '',
        '#mu #eta',
        'Events'
        )

mu_phi = Histogram(
        'lep_0_phi',
        (16, -3.2, 3.2),
        '',
        '#mu #phi',
        'Events'
        )

# Lepton isolation variables
mu_iso_trk = Histogram(
        'lep_0_iso_ptcone40/1000.0/lep_0_pt',
        (20, 0.001, 0.4),
        '',
        '#mu p_{T}^{cone40}/p_{T}',
        'Events'
        )

mu_iso_cal = Histogram(
        'lep_0_iso_etcone20/1000.0/lep_0_et',
        (30, -0.1, 0.4),
        '',
        '#mu E_{T}^{cone20}/E_{T}',
        'Events'
        )

mu_iso_var_trk = Histogram(
        'lep_0_iso_ptvarcone30/1000.0/lep_0_pt',
        (20, 0.001, 0.4),
        '',
        '#mu p_{T}^{varcone30}/p_{T}',
        'Events'
        )

mu_iso_topo_cal = Histogram(
        'lep_0_iso_topoetcone20/1000.0/lep_0_et',
        (30, -0.1, 0.4),
        '',
        '#mu E_{T}^{topocone20}/E_{T}',
        'Events'
        )

met_et = Histogram(
        'met_reco_et',
        (15, 0, 300),
        '',
        'E_{T}^{miss} [GeV]',
        'Events / 20 GeV'
        )

met_eta = Histogram(
        'met_reco_eta',
        (20, -3.0, 3.0),
        '',
        'E_{T}^{miss} #eta',
        'Events'
        )

met_phi = Histogram(
        'met_reco_phi',
        (16, -3.2, 3.2),
        '',
        'E_{T}^{miss} #phi',
        'Events'
        )

jet_multiplicity = Histogram(
        'n_jets',
        (10, 0.5, 10.5),
        '',
        'N_{jets}',
        'Events'
        )

bjet_multiplicity = Histogram(
        'n_bjets',
        (10, 0.5, 10.5),
        '',
        'N_{b-jets}',
        'Events'
        )

jet_0_pt = Histogram(
        'jet_0_pt',
        (15, 0, 300),
        '',
        'Leading jet p_{T} [GeV]',
        'Events / 20 GeV'
        )

jet_0_eta = Histogram(
        'jet_0_eta',
        (20, -3.0, 3.0),
        '',
        'Leading jet #eta',
        'Events'
        )

jet_0_phi = Histogram(
        'jet_0_phi',
        (16, -3.2, 3.2),
        '',
        'Leading jet #phi',
        'Events'
        )

jet_1_pt = Histogram(
        'jet_1_pt',
        (15, 0, 300),
        '',
        'Subleading jet p_{T} [GeV]',
        'Events / 20 GeV'
        )

jet_1_eta = Histogram(
        'jet_1_eta',
        (20, -3.0, 3.0),
        '',
        'Subleading jet #eta',
        'Events'
        )

jet_1_phi = Histogram(
        'jet_1_phi',
        (16, -3.2, 3.2),
        '',
        'Subleading jet #phi',
        'Events'
        )

jet_2_pt = Histogram(
        'jet_2_pt',
        (15, 0, 300),
        '',
        'Third jet p_{T} [GeV]',
        'Events / 20 GeV'
        )

jet_2_eta = Histogram(
        'jet_2_eta',
        (20, -3.0, 3.0),
        '',
        'Third jet #eta',
        'Events'
        )

jet_2_phi = Histogram(
        'jet_2_phi',
        (16, -3.2, 3.2),
        '',
        'Third jet #phi',
        'Events'
        )

mt = Histogram(
        'lephad_mt_lep0_met',
        (15, 0, 300),
        '',
        'm_{T}(E_{T}^{miss},#tau)',
        'Events / 20 GeV'
        )

dphi = Histogram(
        'abs(lephad_dphi)',
        (16, 0, 3.2),
        '',
        '#Delta#phi(#mu,#tau)',
        'Events'
        )

deta = Histogram(
        'abs(lephad_deta)',
        (16, 0, 3.2),
        '',
        '#Delta#eta(#mu,#tau)',
        'Events'
        )

dr = Histogram(
        'abs(lephad_dr)',
        (16, 0, 3.2),
        '',
        '#Delta R(#mu,#tau)',
        'Events'
        )

# Event variables
mu = Histogram(
        'n_avg_int_cor',
        (40, 0, 40),
        '',
        '<#mu>',
        'Events'
        )

nvx = Histogram(
        'n_vx',
        (40, 0, 40),
        '',
        'N_{vx}',
        'Events'
        )

# Quantities for trigger analyses
tau_pt_trig_1gev = Histogram(
        'tau_0_pt',
        (125,25,150),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events'
        )
tau_pt_trig_5gev = Histogram(
        'tau_0_pt',
        (25,25,150),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events'
        )
tau_pt_trig_b1 = Histogram(
        'tau_0_pt',
        (25, 28, 30, 32, 34, 36, 39, 43, 53, 100, 150, 300),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events'
        )
tau_pt_trig_b2  = Histogram(
        'tau_0_pt',
        (25, 28, 30, 32, 34, 36, 39, 43, 48, 54, 62, 72, 85, 100, 125, 150, 300),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events'
        )
tau_pt_trig_b3  = Histogram(
        'tau_0_pt',
        (25, 28, 30, 32, 34, 36, 39, 43, 52, 64, 80, 100, 150, 300),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events'
        )
tau_pt_trig_b4  = Histogram(
        'tau_0_pt',
        (25, 28, 31, 34, 37, 40, 44, 53, 65, 100, 150, 300),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events'
        )

tau_pt_trig_b5 = Histogram(
        'tau_0_pt',
        (20, 0, 200),
        '',
        'Offline #tau p_{T} [GeV]',
        'Events / 10 GeV'
        )

tau_bdt_score_trig = Histogram(
        'tau_0_trig1_HLT_jet_bdt_score',
        (25, 0.5, 1.0),
        '',
        'HLT BDT #tau ID score',
        'Events'
        )

# Weights
NOMINAL_pileup_combined_weight = Histogram(
	'NOMINAL_pileup_combined_weight',
	(30,0.0,3.0),
	'',
	'NOMINAL_pileup_combined_weight',
	'Events'
)
lep_0_NOMINAL_MuEffSF_Reco_QualMedium = Histogram(
        'lep_0_NOMINAL_MuEffSF_Reco_QualMedium',
	(25,0.9,1.15),
        '',
        'lep_0_NOMINAL_MuEffSF_Reco_QualMedium',
        'Events'
)
lep_0_NOMINAL_MuEffSF_IsoGradient = Histogram(
        'lep_0_NOMINAL_MuEffSF_IsoGradient',
	(25,0.9,1.15),
        '',
        'lep_0_NOMINAL_MuEffSF_IsoGradient',
        'Events'
)
lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoIsoGradient = Histogram(
        'lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoIsoGradient',
	(70,0.7,1.4),
        '',
        'lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoIsoGradient',
        'Events'
)
lep_0_NOMINAL_MuEffSF_HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoIsoGradient = Histogram(
        'lep_0_NOMINAL_MuEffSF_HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoIsoGradient',
	(70,0.7,1.4),
        '',
        'lep_0_NOMINAL_MuEffSF_HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoIsoGradient',
        'Events'
)
tau_0_NOMINAL_effSF_VeryLooseLlhEleOLR_electron = Histogram(
        'tau_0_NOMINAL_effSF_VeryLooseLlhEleOLR_electron',
	(30,0.0,3.0),
        '',
        'tau_0_NOMINAL_effSF_VeryLooseLlhEleOLR_electron',
        'Events'
) 
tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM = Histogram(
        'tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM',
	(30,0.0,3.0),
        '',
        'tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM',
        'Events'
) 
tau_0_NOMINAL_TAU_EFF_RECO = Histogram(
        'tau_0_NOMINAL_TAU_EFF_RECO',
	(30,0.0,3.0),
        '',
        'tau_0_NOMINAL_TAU_EFF_RECO',
        'Events'
) 
tau_0_NOMINAL_TAU_EFF_SELECTION = Histogram(
        'tau_0_NOMINAL_TAU_EFF_SELECTION',
	(30,0.0,3.0),
        '',
        'tau_0_NOMINAL_TAU_EFF_SELECTION',
        'Events'
)
