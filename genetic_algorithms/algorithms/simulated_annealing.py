from typing import Union
from genetic_algorithms.algorithms import Algorithm, AlgorithmConfig
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from random import choices
from dataclasses import dataclass
import math


@dataclass
class SimulatedAnnealingConfig(AlgorithmConfig):
    initial_temperature: int = 1000
    cooling_step: float = 0.001


DEFAULT_CONFIG = SimulatedAnnealingConfig()


class SimulatedAnnealing(Algorithm):
    """
    Implementation of the simulated annealing algorithm.

    A version of stochastic hill climbing, that allows going downhills. 
    """

    def __init__(self, config: SimulatedAnnealingConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.temperature = self.config.initial_temperature
        super().__init__(config=config)

    def _calculate_selection_probability(self, old_state_cost: float, new_state_cost: float) -> float:
        return math.exp(-(new_state_cost - old_state_cost) / self.temperature)

    def _update_temperature(self):
        self.temperature = self.config.cooling_step * self.temperature

    def next_state(self, model: Model, state: State) -> Union[State, None]:
        move = next(model.move_generator.random_moves(state))
        new_state = move.make()
        old_state_cost, new_state_cost = model.cost_for(
            state), model.cost_for(new_state)
        if new_state_cost > old_state_cost:
            result = new_state
        else:
            new_state_selection_probability = self._calculate_selection_probability(
                old_state_cost, new_state_cost)
            result = choices([new_state, state], [
                             new_state_selection_probability, 1 - new_state_selection_probability], k=1)[0]
        self._update_temperature()
        return result if not self._is_optimal_state(new_state_cost) else None
