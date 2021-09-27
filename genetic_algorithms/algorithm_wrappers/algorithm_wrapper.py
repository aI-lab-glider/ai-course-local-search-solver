from abc import abstractmethod
from typing import Type, Union
from genetic_algorithms.algorithms import Algorithm
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

    def next_state(self, model: Model, state: State) -> Union[State, None]:
        next_state = self.algorithm.next_state(model, state)
        if next_state:
            self._perform_side_effects(model=model, state=next_state)
        return next_state


class VisualizationWrapper(AlgorithmWrapper):
    """
    Provides visualization to algorithm solutions.
    """
    visualizations = {}

    def __init__subclass__(cls):
        VisualizationWrapper.visualizations[cls.get_corresponding_problem(
        )] = cls

    @staticmethod
    @abstractmethod
    def get_corresponding_problem() -> Type[Model]:
        """
        Returns model type for which this visualization was done
        """
