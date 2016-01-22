"""Uncertainties for the mu+tau ttbar T&P analysis.
"""


# owls-hep imports
from owls_hep.uncertainty import Uncertainty, sum_quadrature, to_overall
from owls_hep.region import Reweighted

class TestSystFlat(Uncertainty):
    @staticmethod
    def name():
        return 'TEST_SYST_FLAT'

    def __call__(self, process, region):
        return (1.1,
                0.9,
                None,
                None)

class TestSystShape(Uncertainty):
    @staticmethod
    def name():
        return 'TEST_SYST_SHAPE'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted('1.2'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted('0.8'))
                ))

class RqcdStat(Uncertainty):
    @staticmethod
    def name():
        return 'RQCD_STAT'

    def __call__(self, process, region):
        return (1.0+0.016,
                1.0-0.016,
                None,
                None)

class MuonEffStat(Uncertainty):
    @staticmethod
    def name():
        return 'MUON_EFF_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_STAT_1up_effSF_RecoMedium'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_STAT_1down_effSF_RecoMedium'))
                ))

class MuonEffSys(Uncertainty):
    @staticmethod
    def name():
        return 'MUON_EFF_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_SYS_1up_effSF_RecoMedium'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_SYS_1down_effSF_RecoMedium'))
                ))

class MuonEffTrigStat(Uncertainty):
    @staticmethod
    def name():
        return 'MUON_EFF_TRIG_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_TrigStatUncertainty_1up_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_TrigStatUncertainty_1down_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ))

class MuonEffTrigSys(Uncertainty):
    @staticmethod
    def name():
        return 'MUON_EFF_TRIG_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_TrigSystUncertainty_1up_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_EFF_TrigSystUncertainty_1down_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'))
                ))

class MuonIsoStat(Uncertainty):
    @staticmethod
    def name():
        return 'MUON_ISO_STAT'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_ISO_STAT_1up_effSF_IsoGradient'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_ISO_STAT_1down_effSF_IsoGradient'))
                ))

class MuonIsoSys(Uncertainty):
    @staticmethod
    def name():
        return 'MUON_ISO_SYS'

    def __call__(self, process, region):
        return (None,
                None,
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_ISO_SYS_1up_effSF_IsoGradient'))
                ),
                self.calculation(
                    process,
                    region.varied(Reweighted(
                        'lep_0_MUON_ISO_SYS_1down_effSF_IsoGradient'))
                ))

class MuonIdSys(Uncertainty):
    @staticmethod
    def name():
        return 'MuonIdSys'

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
    @staticmethod
    def name():
        return 'MuonMsSys'

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
    @staticmethod
    def name():
        return 'MuonScaleSys'

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

