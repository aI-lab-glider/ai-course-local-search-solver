import math
from dataclasses import dataclass
from enum import Enum
from random import choices
from typing import Union

from local_search.algorithms import AlgorithmConfig, SubscribableAlgorithm
from local_search.algorithms.subscribable_algorithm import OptimizationStrategy
from local_search.problems.base.problem import Problem
from local_search.problems.base.state import State


class OnOptimumStrategy(Enum):
    Heat = 'heat'
    Restart = 'restart'
    Terminate = 'terminate'


@dataclass
class SimulatedAnnealingConfig(AlgorithmConfig):
    initial_temperature: int = 1000
    cooling_step: float = 0.001
    min_temperature: float = 1e-8
    on_optimum_strategy: OnOptimumStrategy = OnOptimumStrategy.Terminate
    on_optimum_strategy_repeats: int = 5


DEFAULT_CONFIG = SimulatedAnnealingConfig()


class SimulatedAnnealing(SubscribableAlgorithm):
    """
    Implementation of the simulated annealing algorithm.

    A version of stochastic hill climbing, that allows going downhills. 
    """

    def __init__(self, algorithm_config: SimulatedAnnealingConfig = None, **kwargs):
        self.config = algorithm_config or DEFAULT_CONFIG
        self.temperature = self.config.initial_temperature
        self._optimum_states_found = 0
        super().__init__(algorithm_config=algorithm_config, **kwargs)

    # TODO tests
    def _calculate_selection_probability(self, best_state_cost: float, new_state_cost: float) -> float:
        delta = new_state_cost - best_state_cost 
        return math.exp(-delta / self.temperature)

    # TODO add plot of temperature
    # TODO check
    def _update_temperature(self):
        self.temperature = max(self.temperature - self.config.cooling_step *
                               self.temperature, self.config.min_temperature)

    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        # TODO is it correct. All other algorithms return best state.
        neinghbour = next(self._get_neighbours(
            model, state, is_stochastic=True))
        old_state_cost, new_state_cost = model.cost_for(
            state), model.cost_for(neinghbour)
        if self._is_cost_better_or_same(new_state_cost, old_state_cost):
            result = neinghbour
        else:
            new_state_selection_probability = self._calculate_selection_probability(
                old_state_cost, new_state_cost)
            result = choices([neinghbour, state], [
                             new_state_selection_probability, 1 - new_state_selection_probability], k=1)[0]
        self._update_temperature()
        return result if not self._is_in_optimal_state() else self._on_optimum_state(result)

    def _on_optimum_state(self, state: State):
        self._optimum_states_found += 1
        if self._optimum_states_found > self.config.on_optimum_strategy_repeats:
            return None
        return {
            OnOptimumStrategy.Terminate: lambda _: None,
            OnOptimumStrategy.Restart: self._restart,
            OnOptimumStrategy.Heat: self._heat
        }[self.config.on_optimum_strategy](state)

    def _restart(self, from_state: State):
        # TODO add moves from best state.
        self.steps_from_last_state_update = 0
        return from_state.shuffle()

    def _heat(self, from_state: State):
        self.temperature = self.config.initial_temperature
        self.steps_from_last_state_update = 0
        return from_state
