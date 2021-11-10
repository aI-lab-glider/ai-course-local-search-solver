from abc import ABC, abstractmethod
import random
from typing import Union, Callable

from local_search.algorithms.algorithm_config import AlgorithmConfig
from local_search.algorithms.subscribable_algorithm import SubscribableAlgorithm
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem
from enum import IntEnum, auto
from dataclasses import dataclass


class HCEscapeStrategy(IntEnum):
    RandomRestart = 0
    Perturbation = auto()

@dataclass
class HCConfig(AlgorithmConfig):
    escape_random_restart_probability: float = 0.5
    escape_perturbation_probability: float = 0.5
    escape_perturbation_size: int = 50

DEFAULT_CONFIG = HCConfig()

class HillClimbing(SubscribableAlgorithm, ABC):
    """
    Template for various greedy local search algorithms.
    Supports escaping local optima by random restarts / random perturbations
    """
    def __init__(self, config: HCConfig = None):
        self.config = config or DEFAULT_CONFIG
        self._local_optimum_escapes = 0
        self._escape_strategies = list(HCEscapeStrategy)
        self._escape_probabilities = [0 for _ in self._escape_strategies]
        self._escape_probabilities[HCEscapeStrategy.RandomRestart.value] = self.config.escape_random_restart_probability
        self._escape_probabilities[HCEscapeStrategy.Perturbation.value] = self.config.escape_perturbation_probability
        super().__init__(config=config)

    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        next_state = self._climb_the_hill(model, state)
        return next_state

    @abstractmethod
    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        "there are many ways to climb the hill..."

    def escape_local_optimum(self, model: Problem, state: State, best_state: State) -> Union[State, None]:
        self._local_optimum_escapes += 1
        if self._local_optimum_escapes > self.config.local_optimum_escapes_max >= 0:
            return None
        strategy = random.choices(self._escape_strategies, weights=self._escape_probabilities)[0]
        if strategy == HCEscapeStrategy.RandomRestart:
            return self._random_restart(model)
        if strategy == HCEscapeStrategy.Perturbation:
            return self._perturb(model, self.config.escape_perturbation_size)
