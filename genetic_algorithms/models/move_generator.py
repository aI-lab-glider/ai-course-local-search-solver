from abc import ABC, abstractmethod
from genetic_algorithms.problems.base.state import State
from typing import Generic, TypeVar
from typing import Any, Generator
from genetic_algorithms.problems.base.moves import Move
from random import sample
TState = TypeVar("TState")


class MoveGenerator(ABC):
    def random_moves(self, state: State) -> Generator[Move[Any], None, None]:
        """
        Generates all available moves from state, but moves are performed in a random order.

        CAUTION: below implementation is not an optimal one, because it needs to firstly materialize all available moves, which causes:
        1. memory issues in case of a big problem
        2. speed issues.
        It is recommended, to overwrite this method and define a generator for each problem separatly.
        """
        moves = list(self.available_moves(state))
        return (move for move in sample(moves, len(moves)))

    @ abstractmethod
    def available_moves(self, state: State) -> Generator[Move[Any], None, None]:
        """
        Generates available moves from state
        """
