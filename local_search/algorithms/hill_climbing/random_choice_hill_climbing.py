from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class RandomChoiceHillClimbing(HillClimbing):
    """
    Stochastic variant of hill climbing local search.

    Algorithm works, by randomly sampling the neighborhood
    and selecting a move if it improves the current state.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        neighbour = next(self._get_random_neighbours(model, state))
        if model.improvement(neighbour, state) > 0:
            return neighbour
        return state