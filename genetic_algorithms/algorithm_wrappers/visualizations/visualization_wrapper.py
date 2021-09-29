
from abc import abstractmethod
from typing import Type
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper
from genetic_algorithms.problems import Model


class VisualizationWrapper(AlgorithmWrapper):
    """
    Provides visualization to algorithm solutions.
    """
    visualizations = {}

    def __init_subclass__(cls):
        VisualizationWrapper.visualizations[cls.get_corresponding_problem(
        )] = cls

    @staticmethod
    @abstractmethod
    def get_corresponding_problem() -> Type[Model]:
        """
        Returns model type for which this visualization was done
        """
