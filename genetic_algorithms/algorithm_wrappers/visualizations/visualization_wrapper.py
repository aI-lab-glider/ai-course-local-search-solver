
from abc import abstractmethod
from typing import Type
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmNextNeingbourSubscriber, AlgorithmNextStateSubscriber
from genetic_algorithms.problems import Model
from genetic_algorithms.problems.base.state import State


class VisualizationSubscriber(AlgorithmNextNeingbourSubscriber):
    """
    Provides visualization to algorithm solutions.
    """
    visualizations = {}

    def __init_subclass__(cls):
        VisualizationSubscriber.visualizations[cls.get_corresponding_problem(
        )] = cls

    @staticmethod
    @abstractmethod
    def get_corresponding_problem() -> Type[Model]:
        """
        Returns model type for which this visualization was done
        """
