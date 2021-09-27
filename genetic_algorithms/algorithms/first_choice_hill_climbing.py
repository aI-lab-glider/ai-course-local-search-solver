from dataclasses import dataclass
from typing import Union
from genetic_algorithms.algorithms import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


@dataclass
class FirstChoiceHillClimbingConfig:
    min_count_without_improvements: int = 5


class FirstChoiceHillClimbing(Algorithm):
    """
    Implementaion of stochastic local search. 

    Stochastic version of hill climbing. Algorithm works, by generating one random move,
    applying it to the state and checking if new state is better. 
    In case if new state is better, then algorithm select it and returns, otherwise, it reverts last move.
    """

    def _find_next_state(self, model: Model, state: State) -> Union[State, None]:
        cost_to_outperform = model.cost_for(state)
        for move in model.move_generator.random_moves(state):
            new_state = move.make()
            new_cost = model.cost_for(new_state)
            if new_cost >= cost_to_outperform:
                if new_cost != self._best_cost:
                    self._iter_count_since_best_solution += 1
                else:
                    self._iter_count_since_best_solution = 0
                self._best_cost, self._best_state = new_cost, new_state
                return new_state if not self._is_optimal_state(new_cost) else None
