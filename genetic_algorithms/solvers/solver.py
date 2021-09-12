from abc import ABC, abstractmethod
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.models.algorithm import Algorithm
from dataclasses import dataclass
from time import time


@dataclass
class SolverConfig:
    """ "
    Parameters that are required to correct solver work
    """

    max_iter: int = 1000
    history_size: int = 5


DEFAULT_CONFIG = SolverConfig()


class Solver(ABC):
    def __init__(self, time_limit: int, config: SolverConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.time_limit = time_limit
        self.total_time = None
        self.start_time = None

    def start_timer(self):
        self.start_time = time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time() - self.start_time

    def timeout(self) -> bool:
        return self.wall_time() > self.time_limit

    @abstractmethod
    def solve(self, model: Model, algorithm: Algorithm) -> State:
        """
        Applies some logic to solve a given problem
        """
