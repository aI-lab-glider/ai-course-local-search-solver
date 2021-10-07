import random
from typing import Union
from local_search.algorithms import SubscribableAlgorithm, AlgorithmConfig
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem
import random
from dataclasses import dataclass
import mpmath
from enum import IntEnum, auto


class SAEscapeStrategy(IntEnum):
    RandomRestart = 0
    Perturbation = auto()
    Reheat = auto()

@dataclass
class SimulatedAnnealingConfig(AlgorithmConfig):
    initial_temperature: int = 1000
    cooling_step: float = 0.001
    min_temperature: float = 1e-8
    escape_random_restart_probability: float = 0.33
    escape_perturbation_probability: float = 0.33
    escape_perturbation_size: int = 50
    escape_reheat_probability: float = 0.33


DEFAULT_CONFIG = SimulatedAnnealingConfig()

class SimulatedAnnealing(SubscribableAlgorithm):
    """
    Implementation of the simulated annealing algorithm.

    A version of stochastic hill climbing, that allows going downhills. 
    """

    def __init__(self, config: SimulatedAnnealingConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.temperature = self.config.initial_temperature
        self._local_optimum_escapes = 0
        self._escape_strategies = list(SAEscapeStrategy)
        self._escape_probabilities = [0 for _ in self._escape_strategies]
        self._escape_probabilities[SAEscapeStrategy.RandomRestart.value] = self.config.escape_random_restart_probability
        self._escape_probabilities[SAEscapeStrategy.Perturbation.value] = self.config.escape_perturbation_probability
        self._escape_probabilities[SAEscapeStrategy.Reheat.value] = self.config.escape_reheat_probability
        super().__init__(config=config)

    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        next_state = state
        neighbour = next(self._get_random_neighbours(model, state))

        if model.improvement(neighbour, state) > 0:
            next_state = neighbour
        else:
            transition_probability = self._calculate_transition_probability(model, state, neighbour)
            if random.random() <= transition_probability:
                 next_state = neighbour

        self._update_temperature()
        if self._is_stuck_in_local_optimum():
            next_state = self._escape_local_optimum(next_state)

        return next_state

    # TODO tests
    def _calculate_transition_probability(self, model: Problem, old_state: State, new_state: State) -> float:
        delta = model.improvement(new_state, old_state)
        return mpmath.exp(-delta / self.temperature)

    # TODO add plot of temperature
    # TODO check
    def _update_temperature(self):
        self.temperature = max(self.temperature - self.config.cooling_step *
                               self.temperature, self.config.min_temperature)

    def escape_local_optimum(self, model: Problem, state: State, best_state: State) -> Union[State, None]:
        self._local_optimum_escapes += 1
        if self._local_optimum_escapes > self.config.local_optimum_escapes_max >= 0:
            return None

        strategy = random.choices(self._escape_strategies, weights=self._escape_probabilities)[0]

        if strategy == SAEscapeStrategy.RandomRestart:
            return self._random_restart(model)
        if strategy == SAEscapeStrategy.Perturbation:
            return self._perturb(model, self.config.escape_perturbation_size)
        if strategy == SAEscapeStrategy.Reheat:
            return self._reheat(state)

    def _reheat(self, from_state: State):
        self.temperature = self.config.initial_temperature
        self.steps_from_last_state_update = 0
        return from_state
