from abc import abstractmethod
from local_search.problems.base.state import State
from local_search.problems import Problem


class AlgorithmSubscriber:
    """
    Allows to subscribe to algorithm updates.
    """

    def __init__(self, algorithm):
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

    def on_solution(self, state: State):
        """
        Hook to call when algorithm finds solution
        """
