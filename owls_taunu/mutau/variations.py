"""Common region variations for the mu+tau analysis.
"""


# owls-hep imports
from owls_hep.region import Variation
from owls_hep.expression import variable_substituted, \
        multiplied, divided, anded, ored

class SS(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'lephad_qxq == 1'), weight)

class OS(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'lephad_qxq == -1'), weight)
