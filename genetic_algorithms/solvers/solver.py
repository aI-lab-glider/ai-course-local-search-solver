from abc import ABC, abstractmethod
from genetic_algorithms.models.next_state_provider import NextStateProvider
from genetic_algorithms.problems.base import Model, State
from genetic_algorithms.algorithms import Algorithm
from dataclasses import dataclass
from time import time


@dataclass
class SolverConfig:
    """
    Parameters that are required to correct solver work
    """
    max_iter: int = 1000
    history_size: int = 5
    time_limit: int = 60


DEFAULT_CONFIG = SolverConfig()


class Solver(ABC):
    def __init__(self, config: SolverConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.time_limit = config.time_limit

    def start_timer(self):
        self.start_time = time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time() - self.start_time

    def timeout(self) -> bool:
        return self.wall_time() > self.time_limit

    @abstractmethod
    def solve(self, model: Model, algorithm: NextStateProvider) -> State:
        """
        Applies some logic to solve a given problem
        """
