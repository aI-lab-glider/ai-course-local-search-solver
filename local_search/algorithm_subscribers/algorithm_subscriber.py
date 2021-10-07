from typing import Union
from local_search.problems.base.state import State
from local_search.problems import Problem


class AlgorithmSubscriber:
    """
    Allows to subscribe to algorithm updates.
    """

    def __init__(self, algorithm, **kwargs):
        self.algorithm = algorithm
        algorithm.subscribe(self)

    def on_next_state(self, model: Problem, state: State) -> None:
        """
        Hook to call when algorithm changes state for which it generates neighbourhood
        """

    def on_next_neighbour(self, model: Problem, from_state: State, next_neighbour: State) -> None:
        """
        Hook to call when algorithm makes move and checks new neighbour.
        """

    def on_local_optimum_escape(self, model: Problem, from_state: State, to_state: Union[State, None]) -> None:
        """
        Hook to call when algorithm escapes local optimum. 
        """

    def on_solution(self, model: Problem, solution: State) -> None:
        """
        Hook to call when algorithm finds solution
        """
