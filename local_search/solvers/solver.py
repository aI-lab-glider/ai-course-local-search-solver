from abc import ABC, abstractmethod
from local_search.algorithm_subscribers.algorithm_monitor import AlgorithmMonitor
from local_search.algorithms.algorithm import Algorithm
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm
from local_search.problems.base import Problem, State
from dataclasses import dataclass
from time import time

from local_search.solvers.solver_config import SolverConfig

# TODO
# 1. Solver can write problems solution to files
# 2. Solver should write descriptive files.
# 3. Solver should save statistics
# 4.


# TODO
# Algorithm monitor should have config, and it should have option, that alows to store solutions.
#


# TODO
# Solver will have algorithm monitor inside it. It will be able to turn it on/off.
# Algorithm monitor will expose collected statistics.
# It should be possible to turn on/off statistics that should be visible.
# Solver will also be able to write down a solution file.


DEFAULT_CONFIG = SolverConfig()


class Solver(ABC):

    def __init__(self, config: SolverConfig = None):
        self._config = config or DEFAULT_CONFIG
        self._time_limit = self._config.time_limit

    @property
    def algorithm_monitor(self):
        return AlgorithmMonitor(self._config)

    def start_timer(self):
        self.start_time = time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time() - self.start_time

    def is_timeout(self) -> bool:
        return self.wall_time() > self._time_limit

    @abstractmethod
    def solve(self, model: Problem, algorithm: SubscribableAlgorithm) -> State:
        """
        Applies some logic to solve a given problem
        """
