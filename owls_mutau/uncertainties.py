"""Uncertainties for the mu+tau ttbar T&P analysis.
"""


# owls-hep imports
from owls_hep.uncertainty import Uncertainty, sum_quadrature, to_overall
from owls_hep.variations import Reweighted, ReplaceWeight

# NOTE: Remember to escape * to treat it like a multiplication sign in
# the regular expression
bjet_nominal = 'bjet_sf_MVX_NOMINAL_sf\*bjet_sf_MVX_NOMINAL_ineff_sf'
bjet_var = lambda v, d: 'bjet_sf_MVX_FT_EFF_Eigen_{0}_1{1}_sf*bjet_sf_MVX_FT_EFF_Eigen_{0}_1{1}_ineff_sf'.format(v, d)
configuration = {
    'NAME': 'Default',
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
    'BJET_EIGEN_LIGHT0': (bjet_nominal, bjet_var('LIGHT_0', 'up'), bjet_var('LIGHT_0', 'down')),
    'BJET_EIGEN_LIGHT1': (bjet_nominal, bjet_var('LIGHT_1', 'up'), bjet_var('LIGHT_1', 'down')),
    'BJET_EIGEN_LIGHT2': (bjet_nominal, bjet_var('LIGHT_2', 'up'), bjet_var('LIGHT_2', 'down')),
    'BJET_EIGEN_LIGHT3': (bjet_nominal, bjet_var('LIGHT_3', 'up'), bjet_var('LIGHT_3', 'down')),
    'BJET_EIGEN_LIGHT4': (bjet_nominal, bjet_var('LIGHT_4', 'up'), bjet_var('LIGHT_4', 'down')),
    'BJET_EIGEN_LIGHT5': (bjet_nominal, bjet_var('LIGHT_5', 'up'), bjet_var('LIGHT_5', 'down')),
    'BJET_EIGEN_LIGHT6': (bjet_nominal, bjet_var('LIGHT_6', 'up'), bjet_var('LIGHT_6', 'down')),
    'BJET_EIGEN_LIGHT7': (bjet_nominal, bjet_var('LIGHT_7', 'up'), bjet_var('LIGHT_7', 'down')),
    'BJET_EIGEN_LIGHT8': (bjet_nominal, bjet_var('LIGHT_8', 'up'), bjet_var('LIGHT_8', 'down')),
    'BJET_EIGEN_LIGHT9': (bjet_nominal, bjet_var('LIGHT_9', 'up'), bjet_var('LIGHT_9', 'down')),
    'BJET_EIGEN_LIGHT10': (bjet_nominal, bjet_var('LIGHT_10', 'up'), bjet_var('LIGHT_10', 'down')),
    'BJET_EIGEN_LIGHT11': (bjet_nominal, bjet_var('LIGHT_11', 'up'), bjet_var('LIGHT_11', 'down')),
    'BJET_EIGEN_LIGHT12': (bjet_nominal, bjet_var('LIGHT_12', 'up'), bjet_var('LIGHT_12', 'down')),
    'BJET_EIGEN_LIGHT13': (bjet_nominal, bjet_var('LIGHT_13', 'up'), bjet_var('LIGHT_13', 'down')),
    'BJET_EXTRAPOLATION': (bjet_nominal, 'bjet_sf_MVX_FT_EFF_extrapolation_1up_sf*bjet_sf_MVX_FT_EFF_extrapolation_1up_ineff_sf', 'bjet_sf_MVX_FT_EFF_extrapolation_1down_sf*bjet_sf_MVX_FT_EFF_extrapolation_1down_ineff_sf'),
    'BJET_EXTRAPOLATION_CHARM': (bjet_nominal, 'bjet_sf_MVX_FT_EFF_extrapolation from charm_1up_sf*bjet_sf_MVX_FT_EFF_extrapolation from charm_1up_ineff_sf', 'bjet_sf_MVX_FT_EFF_extrapolation from charm_1down_sf*bjet_sf_MVX_FT_EFF_extrapolation from charm_1down_ineff_sf'),
}

class TestConfiguration(Uncertainty):
    name = 'TEST_CONFIGURATION'

    def __init__(self):
        self._name = configuration['NAME']

    def __repr__(self):
        return self._name

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

class MuonIdSys(Uncertainty):
    name = 'MUON_ID_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process.retreed(configuration[self.name][0]),
                    region
                ),
                self.calculation(
                    process.retreed(configuration[self.name][1]),
                    region
                ))

class MuonMsSys(Uncertainty):
    name = 'MUON_MS_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process.retreed(configuration[self.name][0]),
                    region
                ),
                self.calculation(
                    process.retreed(configuration[self.name][1]),
                    region
                ))

class MuonScaleSys(Uncertainty):
    name = 'MUON_SCALE_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process.retreed(configuration[self.name][0]),
                    region
                ),
                self.calculation(
                    process.retreed(configuration[self.name][1]),
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

MuonEffStat = _define_weight_systematic('MUON_EFF_STAT',
                                        *configuration['MUON_EFF_STAT'])
MuonEffSys = _define_weight_systematic('MUON_EFF_SYS',
                                       *configuration['MUON_EFF_SYS'])
MuonEffTrigStat = _define_weight_systematic('MUON_EFF_TRIG_STAT',
                                            *configuration['MUON_EFF_TRIG_STAT'])
MuonEffTrigSys = _define_weight_systematic('MUON_EFF_TRIG_SYS',
                                           *configuration['MUON_EFF_TRIG_SYS'])
MuonIsoStat = _define_weight_systematic('MUON_ISO_STAT',
                                        *configuration['MUON_ISO_STAT'])
MuonIsoSys = _define_weight_systematic('MUON_ISO_SYS',
                                       *configuration['MUON_ISO_SYS'])
PileupSys = _define_weight_systematic('PRW_SYS',
                                        *configuration['PRW_SYS'])
BJetEigenB0 = _define_weight_systematic('BJET_EIGEN_B0',
                                        *configuration['BJET_EIGEN_B0'])
BJetEigenB1 = _define_weight_systematic('BJET_EIGEN_B1',
                                        *configuration['BJET_EIGEN_B1'])
BJetEigenB2 = _define_weight_systematic('BJET_EIGEN_B2',
                                        *configuration['BJET_EIGEN_B2'])
BJetEigenB3 = _define_weight_systematic('BJET_EIGEN_B3',
                                        *configuration['BJET_EIGEN_B3'])
BJetEigenB4 = _define_weight_systematic('BJET_EIGEN_B4',
                                        *configuration['BJET_EIGEN_B4'])
BJetEigenC0 = _define_weight_systematic('BJET_EIGEN_C0',
                                        *configuration['BJET_EIGEN_C0'])
BJetEigenC1 = _define_weight_systematic('BJET_EIGEN_C1',
                                        *configuration['BJET_EIGEN_C1'])
BJetEigenC2 = _define_weight_systematic('BJET_EIGEN_C2',
                                        *configuration['BJET_EIGEN_C2'])
BJetEigenC3 = _define_weight_systematic('BJET_EIGEN_C3',
                                        *configuration['BJET_EIGEN_C3'])
BJetEigenLight0 = _define_weight_systematic('BJET_EIGEN_LIGHT0',
                                            *configuration['BJET_EIGEN_LIGHT0'])
BJetEigenLight1 = _define_weight_systematic('BJET_EIGEN_LIGHT1',
                                            *configuration['BJET_EIGEN_LIGHT1'])
BJetEigenLight2 = _define_weight_systematic('BJET_EIGEN_LIGHT2',
                                            *configuration['BJET_EIGEN_LIGHT2'])
BJetEigenLight3 = _define_weight_systematic('BJET_EIGEN_LIGHT3',
                                            *configuration['BJET_EIGEN_LIGHT3'])
BJetEigenLight4 = _define_weight_systematic('BJET_EIGEN_LIGHT4',
                                            *configuration['BJET_EIGEN_LIGHT4'])
BJetEigenLight5 = _define_weight_systematic('BJET_EIGEN_LIGHT5',
                                            *configuration['BJET_EIGEN_LIGHT5'])
BJetEigenLight6 = _define_weight_systematic('BJET_EIGEN_LIGHT6',
                                            *configuration['BJET_EIGEN_LIGHT6'])
BJetEigenLight7 = _define_weight_systematic('BJET_EIGEN_LIGHT7',
                                            *configuration['BJET_EIGEN_LIGHT7'])
BJetEigenLight8 = _define_weight_systematic('BJET_EIGEN_LIGHT8',
                                            *configuration['BJET_EIGEN_LIGHT8'])
BJetEigenLight9 = _define_weight_systematic('BJET_EIGEN_LIGHT9',
                                            *configuration['BJET_EIGEN_LIGHT9'])
BJetEigenLight10 = _define_weight_systematic('BJET_EIGEN_LIGHT10',
                                             *configuration['BJET_EIGEN_LIGHT10'])
BJetEigenLight11 = _define_weight_systematic('BJET_EIGEN_LIGHT11',
                                             *configuration['BJET_EIGEN_LIGHT11'])
BJetEigenLight12 = _define_weight_systematic('BJET_EIGEN_LIGHT12',
                                             *configuration['BJET_EIGEN_LIGHT12'])
BJetEigenLight13 = _define_weight_systematic('BJET_EIGEN_LIGHT13',
                                             *configuration['BJET_EIGEN_LIGHT13'])
BJetExtrapolation = _define_weight_systematic('BJET_EXTRAPOLATION',
                                              *configuration['BJET_EXTRAPOLATION'])
# NOTE: Expression with whitespace, doesn't work.
# BJetExtrapolationCharm = _define_weight_systematic('BJET_EXTRAPOLATION_CHARM',
                                                   # *configuration['BJET_EXTRAPOLATION_CHARM'])
