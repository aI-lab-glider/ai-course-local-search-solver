from abc import ABC, abstractmethod
from local_search.algorithms.algorithm import Algorithm
from local_search.problems.base import Problem, State
from dataclasses import dataclass
from time import time


@dataclass
class SolverConfig:
    max_iter: int = 1000
    time_limit: int = 60


DEFAULT_CONFIG = SolverConfig()


class Solver(ABC):
    def __init__(self, config: SolverConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.time_limit = self.config.time_limit

    def start_timer(self):
        self.start_time = time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time() - self.start_time

    def timeout(self) -> bool:
        return self.wall_time() > self.time_limit

    @abstractmethod
    def solve(self, model: Problem, algorithm: Algorithm) -> State:
        """
        Applies some logic to solve a given problem
        """
