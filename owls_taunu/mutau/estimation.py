"""Provides background estimation routines for the mu+tau analysis.
"""

# owls-hep imports
from owls_hep.estimation import Estimation
from owls_hep.uncertainty import Uncertainty

# owls-taunu imports
from owls_taunu.variations import Filtered
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

        # Initialize the components and loop over the rQCD splits
        components = []
        for split, nominal, stat, syst in self._r_qcd[r_qcd_label]:
            r = region.varied(Filtered(split))

            if isinstance(self._calculation, RqcdStat):
                r_qcd = (nominal, nominal+stat, nominal-stat)
            elif isinstance(self._calculation, RqcdSyst):
                r_qcd = (nominal, nominal+syst, nominal-syst)
            else:
                r_qcd = (nominal, nominal, nominal)

            #if process.metadata().get('print_me', False):
                #print('For split {} I\'m using r_qcd = {} for {} and {}'. \
                      #format(split, r_qcd, type(self._calculation), process.label()))

            # Append OS component
            components.append((
                self._luminosity / 1e3,
                False,
                process,
                r.varied(OS())
            ))

            # Append SS component, with rQCD correction
            components.append((
                tuple([-v*self._luminosity / 1e3 for v in r_qcd]),
                False,
                process,
                r.varied(SS())
            ))

        if 'estimation' in process.metadata().get('print_me', []):
            print('OSSS estimation for {} and {} with rQCD label {} and {} '
                  'components'.format(type(self._calculation),
                                      process.label(),
                                      r_qcd_label,
                                      len(components)))

        return components

class SSData(Estimation):
    def __init__(self, calculation, r_qcd):
        # Call superclass initializer
        super(SSData, self).__init__(calculation)

        # Store r_qcd dictionary
        self._r_qcd = r_qcd

    def components(self, process, region):
        # Extract the r_qcd value from the rqcd label
        r_qcd_label = region.metadata()['rqcd']
        # Initialize the components and loop over the rQCD splits
        components = []
        for split, nominal, stat, syst in self._r_qcd[r_qcd_label]:
            r = region.varied(Filtered(split))

            if isinstance(self._calculation, RqcdStat):
                r_qcd = (nominal, nominal+stat, nominal-stat)
            elif isinstance(self._calculation, RqcdSyst):
                r_qcd = (nominal, nominal+syst, nominal-syst)
            else:
                r_qcd = (nominal, nominal, nominal)

            #if process.metadata().get('print_me', False):
                #print('For split {} I\'m using r_qcd = {} for {} and {}'. \
                      #format(split, r_qcd, type(self._calculation), process.label()))

            # Append SS component, with rQCD correction
            components.append((
                r_qcd,
                False,
                process,
                r.varied(SS())
            ))

        if 'estimation' in process.metadata().get('print_me', []):
            print('SSData estimation for {} and {} with rQCD label {} and {} '
                  'components'.format(type(self._calculation),
                                      process.label(),
                                      r_qcd_label,
                                      len(components)))

        return components

class OSData(Estimation):
    def __init__(self, calculation):
        # Call superclass initializer
        super(OSData, self).__init__(calculation)

    def components(self, process, region):
        # Combine components
        return [
            (1.0, False, process, region.varied(OS()))
        ]
