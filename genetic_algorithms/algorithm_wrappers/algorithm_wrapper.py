from abc import abstractmethod
from genetic_algorithms.models.algorithm import Algorithm
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class AlgorithmWrapper(NextStateProvider):
    """
    Allows to add some side effects to algorithm.
    """

    def __init__(self, algorithm: NextStateProvider):
        self.algorithm = algorithm

    @abstractmethod
    def _perform_side_effects(self, model: Model, state: State):
        """
        Performs logic related to the plugin.
        """

    def next_state(self, model: Model, state: State) -> State:
        next_state = self.algorithm.next_state(model, state)
        self._perform_side_effects(model=model, state=next_state)
        return next_state
