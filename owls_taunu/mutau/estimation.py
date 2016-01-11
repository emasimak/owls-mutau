"""Provides background estimation routines for the mu+tau analysis.
"""

# owls-hep imports
from owls_hep.estimation import Estimation
from owls_hep.uncertainty import Uncertainty

# owls-taunu imports
from owls_taunu.mutau.variations import SS, OS


class OSSS(Estimation):
    def __init__(self, calculation, r_qcd, luminosity = 1000):
        # Call superclass initializer
        super(OSSS, self).__init__(calculation)

        # Store r_qcd dictionary
        self._r_qcd = r_qcd

        # Store the luminosity
        self._luminosity = luminosity

    def components(self, process, region):
        # Extract region metadata
        channel = region.metadata()['channel']

        # Figure out r_qcd based on the channel
        r_qcd = self._r_qcd[channel][0]

        # Combine components
        return [
            (1.0 * self._luminosity / 1e3,
             False,
             process,
             region.varied(OS())),
            (-1.0 * r_qcd * self._luminosity / 1e3,
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
        # Extract region metadata
        channel = region.metadata()['channel']

        # Figure out r_qcd based on the channel
        r_qcd = self._r_qcd[channel][0]

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
