from abc import ABC, abstractmethod
from genetic_algorithms.problems.base import Model, Assigment
from dataclasses import dataclass


@dataclass
class SolverConfig:
    """"
    Parameters that are required to correct solver work
    """
    max_iter: int = 1000
    history_size: int = 1


class Solver(ABC):

    def __init__(self, config: SolverConfig):
        self.config = config

    @abstractmethod
    def solve(self, problem: Model) -> Assigment:
        """
        Applies some logic to solve a given problem
        """
