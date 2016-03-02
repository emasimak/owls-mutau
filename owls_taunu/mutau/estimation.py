"""Provides background estimation routines for the mu+tau analysis.
"""

# owls-hep imports
from owls_hep.estimation import Estimation
from owls_hep.uncertainty import Uncertainty

# owls-taunu imports
from owls_taunu.mutau.variations import SS, OS
from owls_taunu.mutau.uncertainties import RqcdSyst, RqcdStat


class OSSS(Estimation):
    def __init__(self, calculation, r_qcd, luminosity = 1000):
        # Call superclass initializer
        super(OSSS, self).__init__(calculation)

        # Store r_qcd dictionary
        self._r_qcd = r_qcd

        # Store the luminosity
        self._luminosity = luminosity

    def components(self, process, region):
        # Extract the r_qcd value from the rqcd label
        r_qcd_label = region.metadata()['rqcd']
        nominal, stat, syst = self._r_qcd[r_qcd_label]
        if isinstance(self._calculation, RqcdStat):
            r_qcd = (nominal, nominal+stat, nominal-stat)
        elif isinstance(self._calculation, RqcdSyst):
            r_qcd = (nominal, nominal+syst, nominal-syst)
        else:
            r_qcd = (nominal, nominal, nominal)

        #if process.metadata().get('print_me', False):
            #print('I\'m using r_qcd = {} for {} and {}'. \
                  #format(r_qcd, type(self._calculation), process.label()))

        # Combine components
        return [
            (self._luminosity / 1e3,
             False,
             process,
             region.varied(OS())),
            (tuple([-v*self._luminosity / 1e3 for v in r_qcd]),
             False,
             process,
             region.varied(SS()))
        ]

class SSData(Estimation):
    def __init__(self, calculation, r_qcd):
        # Call superclass initializer
        super(SSData, self).__init__(calculation)

        # Store r_qcd dictionary
        self._r_qcd = r_qcd

    def components(self, process, region):
        # Extract the r_qcd value from the rqcd label
        r_qcd_label = region.metadata()['rqcd']
        nominal, stat, syst = self._r_qcd[r_qcd_label]
        if isinstance(self._calculation, RqcdStat):
            r_qcd = (nominal, nominal+stat, nominal-stat)
        elif isinstance(self._calculation, RqcdSyst):
            r_qcd = (nominal, nominal+syst, nominal-syst)
        else:
            r_qcd = nominal

        #if process.metadata().get('print_me', False):
            #print('I\'m using r_qcd = {} for {} and {}'. \
                  #format(r_qcd, type(self._calculation), process.label()))

        # Combine components
        return [
            (r_qcd, False, process, region.varied(SS()))
        ]

class OSData(Estimation):
    def __init__(self, calculation):
        # Call superclass initializer
        super(OSData, self).__init__(calculation)

    def components(self, process, region):
        # Combine components
        return [
            (1.0, False, process, region.varied(OS()))
        ]
