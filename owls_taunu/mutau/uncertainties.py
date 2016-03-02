"""Uncertainties for the mu+tau ttbar T&P analysis.
"""


# owls-hep imports
from owls_hep.uncertainty import Uncertainty, sum_quadrature, to_overall
from owls_hep.region import Reweighted

# owls-taunu imports
from owls_taunu.variations import ReplaceWeight

class TestSystFlat(Uncertainty):
    name = 'TEST_SYST_FLAT'

    def __call__(self, process, region):
        return (1.1,
                0.9,
                None,
                None)

class TestSystShape(Uncertainty):
    name = 'TEST_SYST_SHAPE'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted('tau_0_jet_bdt_score+1.0'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted('tau_0_jet_bdt_score-0.10'))
                ))

class RqcdStat(Uncertainty):
    name = 'RQCD_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(process, region),
                self.calculation(process, region))

class RqcdSyst(Uncertainty):
    name = 'RQCD_SYST'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(process, region),
                self.calculation(process, region))

class MuonEffStat(Uncertainty):
    name = 'MUON_EFF_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_RecoMedium',
                        'lep_0_MUON_EFF_STAT_1up_effSF_RecoMedium'))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_RecoMedium',
                        'lep_0_MUON_EFF_STAT_1down_effSF_RecoMedium'))
                ))

class MuonEffSys(Uncertainty):
    name = 'MUON_EFF_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_RecoMedium',
                        'lep_0_MUON_EFF_SYS_1up_effSF_RecoMedium'))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_RecoMedium',
                        'lep_0_MUON_EFF_SYS_1down_effSF_RecoMedium'))
                ))

class MuonEffTrigStat(Uncertainty):
    name = 'MUON_EFF_TRIG_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
                        'lep_0_MUON_EFF_TrigStatUncertainty_1up_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
                        'lep_0_MUON_EFF_TrigStatUncertainty_1down_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ))

class MuonEffTrigSys(Uncertainty):
    name = 'MUON_EFF_TRIG_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
                        'lep_0_MUON_EFF_TrigSystUncertainty_1up_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT',
                        'lep_0_MUON_EFF_TrigSystUncertainty_1down_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ))

class MuonIsoStat(Uncertainty):
    name = 'MUON_ISO_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_IsoGradient',
                        'lep_0_MUON_ISO_STAT_1up_effSF_IsoGradient'))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_IsoGradient',
                        'lep_0_MUON_ISO_STAT_1down_effSF_IsoGradient'))
                ))

class MuonIsoSys(Uncertainty):
    name = 'MUON_ISO_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_IsoGradient',
                        'lep_0_MUON_ISO_SYS_1up_effSF_IsoGradient'))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(
                        'lep_0_NOMINAL_effSF_IsoGradient',
                        'lep_0_MUON_ISO_SYS_1down_effSF_IsoGradient'))
                ))

class MuonIdSys(Uncertainty):
    name = 'MUON_ID_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process.retreed('MUONS_ID_1up'),
                    region
                ),
                self.calculation(
                    process.retreed('MUONS_ID_1down'),
                    region
                ))

class MuonMsSys(Uncertainty):
    name = 'MUON_MS_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process.retreed('MUONS_MS_1up'),
                    region
                ),
                self.calculation(
                    process.retreed('MUONS_MS_1down'),
                    region
                ))

class MuonScaleSys(Uncertainty):
    name = 'MUON_SCALE_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process.retreed('MUONS_SCALE_1up'),
                    region
                ),
                self.calculation(
                    process.retreed('MUONS_SCALE_1down'),
                    region
                ))

class WeightSystematicBase(Uncertainty):
    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(self.nominal, self.up))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(self.nominal, self.down))
                ))


def _define_weight_systematic(name, nominal, up, down):
    return type(name,
                (WeightSystematicBase,),
                dict(name=name, nominal=nominal, up=up, down=down))

# NOTE: Remember to escape * to treat it like a multiplication sign in
# the regular expression
BJetEigenB0 = _define_weight_systematic(
    'BJET_EIGEN_B0',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_0_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_B_0_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_0_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_B_0_1up_ineff_sf')
BJetEigenB1 = _define_weight_systematic(
    'BJET_EIGEN_B1',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_1_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_B_1_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_1_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_B_1_1up_ineff_sf')
BJetEigenB2 = _define_weight_systematic(
    'BJET_EIGEN_B2',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_2_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_B_2_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_2_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_B_2_1up_ineff_sf')
BJetEigenB3 = _define_weight_systematic(
    'BJET_EIGEN_B3',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_3_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_B_3_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_3_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_B_3_1up_ineff_sf')
BJetEigenB4 = _define_weight_systematic(
    'BJET_EIGEN_B4',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_4_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_B_4_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_B_4_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_B_4_1up_ineff_sf')
BJetEigenC0 = _define_weight_systematic(
    'BJET_EIGEN_C0',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_0_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_C_0_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_0_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_C_0_1up_ineff_sf')
BJetEigenC1 = _define_weight_systematic(
    'BJET_EIGEN_C1',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_1_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_C_1_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_1_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_C_1_1up_ineff_sf')
BJetEigenC2 = _define_weight_systematic(
    'BJET_EIGEN_C2',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_2_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_C_2_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_2_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_C_2_1up_ineff_sf')
BJetEigenC3 = _define_weight_systematic(
    'BJET_EIGEN_C3',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_3_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_C_3_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_C_3_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_C_3_1up_ineff_sf')
BJetEigenLight0 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT0',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_0_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_0_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_0_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_0_1up_ineff_sf')
BJetEigenLight1 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT1',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_1_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_1_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_1_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_1_1up_ineff_sf')
BJetEigenLight2 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT2',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_2_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_2_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_2_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_2_1up_ineff_sf')
BJetEigenLight3 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT3',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_3_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_3_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_3_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_3_1up_ineff_sf')
BJetEigenLight4 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT4',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_4_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_4_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_4_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_4_1up_ineff_sf')
BJetEigenLight5 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT5',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_5_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_5_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_5_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_5_1up_ineff_sf')
BJetEigenLight6 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT6',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_6_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_6_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_6_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_6_1up_ineff_sf')
BJetEigenLight7 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT7',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_7_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_7_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_7_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_7_1up_ineff_sf')
BJetEigenLight8 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT8',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_8_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_8_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_8_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_8_1up_ineff_sf')
BJetEigenLight9 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT9',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_9_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_9_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_9_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_9_1up_ineff_sf')
BJetEigenLight10 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT10',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_10_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_10_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_10_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_10_1up_ineff_sf')
BJetEigenLight11 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT11',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_11_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_11_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_11_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_11_1up_ineff_sf')
BJetEigenLight12 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT12',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_12_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_12_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_12_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_12_1up_ineff_sf')
BJetEigenLight13 = _define_weight_systematic(
    'BJET_EIGEN_LIGHT13',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_13_1down_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_13_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_Eigen_Light_13_1up_sf*bjet_sf_MVX_FT_EFF_Eigen_Light_13_1up_ineff_sf')
BJetExtrapolation = _define_weight_systematic(
    'BJET_EXTRAPOLATION',
    'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    'bjet_sf_MVX_FT_EFF_extrapolation_1down_sf*bjet_sf_MVX_FT_EFF_extrapolation_1down_ineff_sf',
    'bjet_sf_MVX_FT_EFF_extrapolation_1up_sf*bjet_sf_MVX_FT_EFF_extrapolation_1up_ineff_sf')
# NOTE: Expression with whitespace, doesn't work.
#BJetExtrapolationCharm = _define_weight_systematic(
    #'BJET_EXTRAPOLATION_CHARM',
    #'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf',
    #'bjet_sf_MVX_FT_EFF_extrapolation from charm_1down_sf*bjet_sf_MVX_FT_EFF_extrapolation from charm_1down_ineff_sf',
    #'bjet_sf_MVX_FT_EFF_extrapolation from charm_1up_sf*bjet_sf_MVX_FT_EFF_extrapolation from charm_1up_ineff_sf')
