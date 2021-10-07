from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class FirstChoiceHillClimbing(HillClimbing):
    """
    Implementation of hill climbing local search.

    Very basic version of hill climbing. Algorithm works, by generating one move,
    applying it to the state and checking if new state is better. 
    In case if new state is better, then algorithm select it and returns, otherwise, it tries another.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        for neighbour in self._get_neighbours(model, state):
            if model.improvement(neighbour, state) > 0:
                return neighbour
        return state
