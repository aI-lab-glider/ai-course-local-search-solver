from abc import ABC, abstractmethod
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.models.algorithm import Algorithm
from dataclasses import dataclass


@dataclass
class SolverConfig:
    """"
    Parameters that are required to correct solver work
    """
    max_iter: int = 1000
    history_size: int = 5


DEFAULT_CONFIG = SolverConfig()


class Solver(ABC):

    def __init__(self, algorithm: Algorithm, config: SolverConfig = None):
        self.algorithm = algorithm
        self.config = config or DEFAULT_CONFIG

    @abstractmethod
    def solve(self, model: Model) -> State:
        """
        Applies some logic to solve a given problem
        """
