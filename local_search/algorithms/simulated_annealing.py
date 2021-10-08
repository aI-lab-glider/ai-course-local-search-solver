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
    initial_temperature: int = 5
    cooling_step: float = 0.999
    min_temperature: float = 1e-10
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
        self.cooling_time = 0
        super().__init__(config=config)

    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        # TODO:
        # — find random neighbour (self._get_random_neighbours + `next` to read a single element)
        # — if the neighbour is better then mark is as the next state
        # — otherwise calculate the probability of transition using self._calculate_transition_probability
        #   * use random.random() to check whether the neighbor should be a new state
        # — update temperature
        # — return the new state
        next_state = state
        neighbour = next(self._get_random_neighbours(model, state))

        if model.improvement(neighbour, state) > 0:
            next_state = neighbour
        else:
            transition_probability = self._calculate_transition_probability(model, state, neighbour)
            if random.random() <= transition_probability:
                next_state = neighbour

        self._update_temperature()
        return next_state

    def _calculate_transition_probability(self, model: Problem, old_state: State, new_state: State) -> float:
        # TODO:
        # - calculate probability of transition according to the metropolis function
        #   p = exp(delta / temperature)
        #   where: delta is the improvement of the objective function (model has a corresponding method)
        # - use mpmath to calculate the exponential
        delta = model.improvement(new_state, old_state)
        return mpmath.exp(delta / self.temperature)

    def _update_temperature(self):
        # TODO:
        # — update self.temperature according to the exponential decrease function:
        #   T_k = T * a^k
        #   where 'a' can be found in the config as the cooling_step
        #   and k is stored as self.cooling_time
        # - update self.cooling_time
        # - the temperature can't go below self.config.min_temperature
        self.temperature = max(self.temperature * (self.config.cooling_step ** self.cooling_time), self.config.min_temperature)
        self.cooling_time += 1

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
        # TODO:
        # — restore the initial temperature from config
        # — reset cooling schedule (self.cooling_steps)
        # — reset self.steps_from_last_state_update
        # return the from state
        self.temperature = self.config.initial_temperature
        self.steps_from_last_state_update = 0
        self.cooling_time = 0
        return from_state
