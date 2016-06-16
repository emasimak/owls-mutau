"""Common region variations for the mu+tau analysis.
"""

# owls-hep imports
from owls_hep.variations import Variation
from owls_hep.expression import anded

class OneProng(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'tau_0_n_tracks == 1'), weight)

class ThreeProng(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'tau_0_n_tracks  == 3'), weight)
