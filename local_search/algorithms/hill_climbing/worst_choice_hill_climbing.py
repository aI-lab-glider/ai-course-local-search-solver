from typing import Union
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing
from local_search.problems.base.state import State
from local_search.problems.base.problem import Problem


class WorstChoiceHillClimbing(HillClimbing):
    """
    Implementation of hill climbing local search.

    Pretty exotic version of hill climbing. Algorithm works, by checking all the available moves
    and selecting the worst one that improves the current state.
    """

    def _climb_the_hill(self, model: Problem, state: State) -> Union[State, None]:
        worst_improving_state = None
        for neighbour in self._get_neighbours(model, state):
            if model.improvement(neighbour, state) > 0:
                if worst_improving_state is None:
                    worst_improving_state = neighbour
                elif model.improvement(neighbour, worst_improving_state) < 0:
                    worst_improving_state = neighbour

        if worst_improving_state is None:
            return state
        return worst_improving_state
