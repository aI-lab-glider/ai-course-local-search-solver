from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing

from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem

class BestChoiceHillClimbing(HillClimbing):
    """
    Implementation of hill climbing local search.

    The most known version of hill climbing.
    Algorithm works, by checking all the available moves
    and selecting the best one that improves the current state.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        best_improving_state = state
        for neighbour in self._get_neighbours(model, state):
            if model.improvement(neighbour, state) > 0:
                if best_improving_state is None:
                    best_improving_state = neighbour
                elif model.improvement(neighbour, best_improving_state) > 0:
                    best_improving_state = neighbour
        return best_improving_state
