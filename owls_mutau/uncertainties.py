"""Uncertainties for the mu+tau ttbar T&P analysis.
"""


# owls-hep imports
from owls_hep.uncertainty import Uncertainty, sum_quadrature, to_overall
from owls_hep.variations import Reweighted, ReplaceWeight

configuration = {}

class TestConfiguration(Uncertainty):
    name = 'TEST_CONFIGURATION'

    def __init__(self):
        pass

    def __repr__(self):
        return configuration['NAME']

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
    def _get_nominal(self):
        return configuration[self.name][0]

    def _get_up(self):
        return configuration[self.name][1]

    def _get_down(self):
        return configuration[self.name][2]

    def __call__(self, process, region):
        if 'syst' in process.metadata().get('print_me', []):
            print('Calling {} with\n  nominal = {}\n  up = {}\n  down = {}'.\
                  format(self.name,
                         self._get_nominal(),
                         self._get_up(),
                         self._get_down()))
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(self._get_nominal(),
                                                self._get_up()))
                ),
                self.calculation(
                    process,
                    region.varied(ReplaceWeight(self._get_nominal(),
                                                self._get_down()))
                ))


def _define_weight_systematic(name):
    return type(name,
                (WeightSystematicBase,),
                dict(name=name))

MuonEffStat = _define_weight_systematic('MUON_EFF_STAT')
MuonEffSys = _define_weight_systematic('MUON_EFF_SYS')
MuonEffTrigStat = _define_weight_systematic('MUON_EFF_TRIG_STAT')
MuonEffTrigSys = _define_weight_systematic('MUON_EFF_TRIG_SYS')
MuonIsoStat = _define_weight_systematic('MUON_ISO_STAT')
MuonIsoSys = _define_weight_systematic('MUON_ISO_SYS')
PileupSys = _define_weight_systematic('PRW_SYS')
TauIdSys = _define_weight_systematic('TAU_ID_SYS')
TauRecoSys = _define_weight_systematic('TAU_RECO_SYS')
TauEleOlrSys = _define_weight_systematic('TAU_ELEOLR_SYS')
BJetEigenB0 = _define_weight_systematic('BJET_EIGEN_B0')
BJetEigenB1 = _define_weight_systematic('BJET_EIGEN_B1')
BJetEigenB2 = _define_weight_systematic('BJET_EIGEN_B2')
BJetEigenB3 = _define_weight_systematic('BJET_EIGEN_B3')
BJetEigenB4 = _define_weight_systematic('BJET_EIGEN_B4')
BJetEigenC0 = _define_weight_systematic('BJET_EIGEN_C0')
BJetEigenC1 = _define_weight_systematic('BJET_EIGEN_C1')
BJetEigenC2 = _define_weight_systematic('BJET_EIGEN_C2')
BJetEigenC3 = _define_weight_systematic('BJET_EIGEN_C3')
BJetEigenLight0 = _define_weight_systematic('BJET_EIGEN_LIGHT0')
BJetEigenLight1 = _define_weight_systematic('BJET_EIGEN_LIGHT1')
BJetEigenLight2 = _define_weight_systematic('BJET_EIGEN_LIGHT2')
BJetEigenLight3 = _define_weight_systematic('BJET_EIGEN_LIGHT3')
BJetEigenLight4 = _define_weight_systematic('BJET_EIGEN_LIGHT4')
BJetEigenLight5 = _define_weight_systematic('BJET_EIGEN_LIGHT5')
BJetEigenLight6 = _define_weight_systematic('BJET_EIGEN_LIGHT6')
BJetEigenLight7 = _define_weight_systematic('BJET_EIGEN_LIGHT7')
BJetEigenLight8 = _define_weight_systematic('BJET_EIGEN_LIGHT8')
BJetEigenLight9 = _define_weight_systematic('BJET_EIGEN_LIGHT9')
BJetEigenLight10 = _define_weight_systematic('BJET_EIGEN_LIGHT10')
BJetEigenLight11 = _define_weight_systematic('BJET_EIGEN_LIGHT11')
BJetEigenLight12 = _define_weight_systematic('BJET_EIGEN_LIGHT12')
BJetEigenLight13 = _define_weight_systematic('BJET_EIGEN_LIGHT13')
BJetExtrapolation = _define_weight_systematic('BJET_EXTRAPOLATION')
BJetExtrapolationCharm = _define_weight_systematic('BJET_EXTRAPOLATION_CHARM')
