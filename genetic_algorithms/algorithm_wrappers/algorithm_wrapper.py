from abc import abstractmethod
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems import Model


class AlgorithmSubscriber:
    """
    Allows to subscribe to algorithm updates.
    """

    def __init__(self, algorithm):
        self.algorithm = algorithm
        algorithm.subscribe(self)

    def on_next_state(self, model: Model, state: State) -> None:
        """
        Hook to call when algorithm changes state for which it generates neighbourhood
        """

    def on_next_neighbour(self, model: Model, from_state: State, next_neighbour: State) -> None:
        """
        Hook to call when algorithm makes move and checks new neighbour.
        """

    def on_solution(self, state: State):
        """
        Hook to call when algorithm finds solution
        """
