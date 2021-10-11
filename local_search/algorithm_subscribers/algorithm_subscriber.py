from typing import Union
from local_search.problems import Problem, State


class AlgorithmSubscriber:
    """
    Allows to subscribe to algorithm updates.
    """

    def __init__(self):
        self.__algorithm = None

    @property
    def algorithm(self) -> 'Algorithm':
        if self.__algorithm is None:
            raise AttributeError(
                f'{type(self).__name__} is not subscribed to any algorithm.')
        return self.__algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        if self.__algorithm is not None:
            raise AttributeError(
                f'{type(self).__name__} is already subscribed to {type(self.__algorithm).__name__}.')
        self.__algorithm = algorithm

    def bind(self, algorithm):
        """
        Starts tracking algorithm. Once subscriber is binded it cannot be unbinded.
        """
        self.algorithm = algorithm

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
