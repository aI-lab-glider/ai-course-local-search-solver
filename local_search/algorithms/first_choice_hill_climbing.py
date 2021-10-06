from typing import Union
from local_search.algorithms import SubscribableAlgorithm
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class FirstChoiceHillClimbing(SubscribableAlgorithm):
    """
    Implementaion of stochastic local search. 

    Stochastic version of hill climbing. Algorithm works, by generating one random move,
    applying it to the state and checking if new state is better. 
    In case if new state is better, then algorithm select it and returns, otherwise, it reverts last move.
    """

    def _find_next_state(self, model: Problem, state: State) -> Union[State, None]:
        cost_to_outperform = model.cost_for(state)
        best_state = state
        for neingbour in self._get_neighbours(model, state, True):
            new_cost = model.cost_for(neingbour)
            if self._is_cost_strictly_better(new_cost, cost_to_outperform):
                best_state = neingbour
                break
        return best_state if not self._is_in_optimal_state() else None
