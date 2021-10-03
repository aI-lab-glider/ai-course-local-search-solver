from abc import abstractmethod
from genetic_algorithms.models.next_state_provider import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems import Model


class AlgorithmNextStateSubscriber:
    """
    Allows to add some side effects to algorithm.
    """

    def __init__(self, algorithm: Algorithm):
        self.algorithm = algorithm

    @abstractmethod
    def _perform_side_effects(self, model: Model, state: State, **kwargs):
        """
        Performs logic related to the plugin.
        """

    def notify(self, model: Model, state: State, **kwargs) -> None:
        if state:
            self._perform_side_effects(model, state, **kwargs)
        else:
            self._on_solution_found(state=state)

    def _on_solution_found(self, state: State):
        """
        Hook that is called when solution is found.
        """

class AlgorithmNextNeingbourSubscriber(AlgorithmNextStateSubscriber):
    def notify(self, model: Model, from_state: State, next_neighbour: State):
        super().notify(model, from_state, next_neighbour=next_neighbour)    
