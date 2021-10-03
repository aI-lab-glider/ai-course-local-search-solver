from dataclasses import dataclass
from genetic_algorithms.algorithms.exceptions import NoSolutionFoundError
from typing import Union
from genetic_algorithms.algorithms import SubscribableAlgorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class FirstChoiceHillClimbing(SubscribableAlgorithm):
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
            if self._is_cost_better(new_cost, cost_to_outperform):
                self._best_cost, self._best_state = new_cost, new_state
                return new_state if not self._is_in_optimal_state() else None
        raise NoSolutionFoundError()
