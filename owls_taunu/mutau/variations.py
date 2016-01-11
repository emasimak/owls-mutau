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

class SS(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'lephad_qxq == 1'), weight)

class OS(Variation):
    def __call__(self, selection, weight):
        return (anded(selection, 'lephad_qxq == -1'), weight)

class Triggered(Variation):
    """A region variation that ANDs a trigger variable into the selection.
    """

    def __init__(self, trigger_name, matched = None, matchvar = None):
        """Initializes a new instance of the Triggered class.

        Args:
                trigger_name:   The expression to incorporate into the region
                                to select the trigger
                matched:        Specifies if the trigger should also be
                                matched in the event
        """
        # Store the trigger_name
        self._trigger_name = trigger_name
        self._matched = matched
        if matchvar is not None:
            self._trigger_match_variable = matchvar
        else:
            self._trigger_match_variable = 'tau_0_trig_' + self._trigger_name

    def desc(self):
        """Returns a description of the variation.
        """
        return self._trigger_name


    def state(self):
        """Returns a representation of the variation's internal state.
        """
        if self._matched is not None:
            return (self._trigger_name,
                    self._matched,
                    self._trigger_match_variable)
        else:
            return (self._trigger_name,)

    def __call__(self, selection, weight):
        """Add's an expression to a region's weight.

        Args:
            selection: The existing selection expression
            weight: The existing weight expression

        Returns:
            A tuple of the form (varied_selection, varied_weight).
        """
        if self._matched is True:
            return (anded(selection,
                          self._trigger_name,
                          self._trigger_match_variable), weight)
        elif self._matched is False:
            return (anded(selection,
                          self._trigger_name,
                          '!' + self._trigger_match_variable), weight)
        else:
            return (anded(selection, self._trigger_name), weight)

    def __str__(self):
        """Return a string representation of the variation.
        """
        if self._matched is True:
            return 'Triggered({0} && {1})'. \
                    format(self._trigger_name,
                           self._trigger_match_variable)
        elif self._matched is False:
            return 'Triggered({0} && !{1})'. \
                    format(self._trigger_name,
                           self._trigger_match_variable)
        else:
            return 'Triggered({0})'.format(self._trigger_name)

class Filtered(Variation):
    """A region variation that ANDs a selection and optionally a weight
    variable into the selection.
    """

    def __init__(self, selection, weight = None):
        """Initializes a new instance of the Filtere class.

        Args:
                selection:      The expression to incorporate into the region
                                to filter out events
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
