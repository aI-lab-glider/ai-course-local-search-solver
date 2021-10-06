from typing import Union
from local_search.algorithms import SubscribableAlgorithm
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class HillClimbing(SubscribableAlgorithm):
    """
    Implementation of basic hill climbing (also known under the name "greedy local search")

    Algorithm works in the way that it searches neighbourhood by maikng all possible moves
    and greedy selects the best neingboor available from the current state.
    """

    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        best_state = state
        best_state_cost = model.cost_for(state)
        for neighbour in self._get_neighbours(model, state):
            new_state_cost = model.cost_for(neighbour)
            if self._is_cost_better_or_same(new_state_cost, best_state_cost):
                (best_state, best_state_cost) = (neighbour, new_state_cost)
        return best_state if not self._is_in_optimal_state() else None
