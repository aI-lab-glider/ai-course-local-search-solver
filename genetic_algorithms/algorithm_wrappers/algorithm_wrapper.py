from abc import abstractmethod
from typing import Type, Union
from genetic_algorithms.algorithms.algorithm import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems import Model


class AlgorithmSubscriber:
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

    def update(self, model: Model, state: State) -> Union[State, None]:
        next_state = self.algorithm.next_state(model, state)
        if next_state:
            self._perform_side_effects(model=model, state=next_state)
        else:
            self._on_solution_found(state=state)
        return next_state

    def _on_solution_found(self, state: State):
        """
        Hook that is called when solution is found.
        """
