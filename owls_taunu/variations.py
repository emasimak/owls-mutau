"""Common region variations for the mu+tau analysis.
"""


# owls-hep imports
from owls_hep.region import Variation
from owls_hep.expression import variable_negated, variable_substituted, \
        multiplied, divided, anded, ored

class OneProng(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'tau_0_n_tracks == 1'), weight)

class ThreeProng(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'tau_0_n_tracks  == 3'), weight)

class Filtered(Variation):
    """A region variation that ANDs a selection and optionally a weight
    variable into the selection.
    """

    def __init__(self, selection, weight = None):
        """Initializes a new instance of the Filtered class.

        Args:
                selection:      The expression to incorporate into the region
                                to filter out events
                weight:         An optional weight to apply to the event
        """
        # Store the trigger_name
        self._selection = selection
        self._weight = weight

    def state(self):
        """Returns a representation of the variation's internal state.
        """
        if self._weight is None:
            return (self._selection,)
        else:
            return (self._selection, self._weight)

    def __call__(self, selection, weight):
        """Add's an expression to a region's weight.

        Args:
            selection: The existing selection expression
            weight: The existing weight expression

        Returns:
            A tuple of the form (varied_selection, varied_weight).
        """
        if self._weight is not None:
            return (anded(selection, self._selection),
                    multiplied(weight, self._weight))
        else:
            return (anded(selection, self._selection), weight)

    def __str__(self):
        """Return a string representation of the variation.
        """
        if self._weight is not None:
            return 'Filtered({0}, {1})'.format(self._selection, self._weight)
        else:
            return 'Filtered({0})'.format(self._selection)

class ReplaceWeight(Variation):
    """A region variation that replaces a weight (single event weight or
    combination thereof) with a new weight (e.g. a systematic variation).
    """

    def __init__(self, weight, variation):
        """Initializes a new instance of the ReplaceWeight class

        Args:
                weight:         Weight in the form of a regular expression
                variation:      Variation to replace weight
        """
        # Store the trigger_name
        self._weight = weight
        self._variation = variation

    def state(self):
        """Returns a representation of the variation's internal state.
        """
        return (self._weight, self._variation)

    def __call__(self, selection, weight):
        """Add's an expression to a region's weight.

        Args:
            selection: The existing selection expression
            weight: The existing weight expression

        Returns:
            A tuple of the form (varied_selection, varied_weight).
        """
        return (selection,
                variable_substituted(weight, self._weight, self._variation))

    def __str__(self):
        """Return a string representation of the variation.
        """
        return 'ReplaceWeight({0})'.format(self._variation)
