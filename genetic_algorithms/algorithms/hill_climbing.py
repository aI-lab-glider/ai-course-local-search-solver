from typing import Union
from genetic_algorithms.algorithms import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class HillClimbing(Algorithm):
    """
    Implementation of basic hill climbing (also known under the name "greedy local search")

    Algorithm works in the way that it searches neighbourhood by maikng all possible moves
    and greedy selects the best neingboor available from the current state.
    """

    def _find_next_state(self, model: Model, state: State) -> Union[State, None]:
        best_state = state
        best_state_cost = model.cost_for(state)
        for move in model.move_generator.available_moves(state):
            new_state = move.make()
            new_state_cost = model.cost_for(new_state)
            if self._is_cost_better(new_state_cost, best_state_cost):
                (best_state, best_state_cost) = (new_state, new_state_cost)
        return best_state if not self._is_optimal_state(best_state_cost) else None
