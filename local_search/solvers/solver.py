from abc import ABC, abstractmethod
from local_search.algorithm_subscribers.algorithm_monitor import AlgorithmMonitor
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm
from local_search.problems.base import Problem, State
from time import time
import atexit
from local_search.solvers.solver_config import SolverConfig

DEFAULT_CONFIG = SolverConfig()


class Solver(ABC):

    def __init__(self, config: SolverConfig = None):
        self._config = config or DEFAULT_CONFIG
        self._time_limit = self._config.time_limit
        self._is_terminated = False
        atexit.register(self.on_exit)

    def on_exit(self):
        self._is_terminated = True

    @property
    def is_terminated(self):
        return self.is_timeout() or self._is_terminated

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
