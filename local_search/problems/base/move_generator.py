from abc import ABC, abstractmethod
from random import sample
from typing import Generator, TypeVar

from local_search.problems.base.moves import Move
from local_search.problems.base.state import State


class MoveGenerator(ABC):
    def random_moves(self, state: State) -> Generator[Move[State], None, None]:
        """
        Generates all available moves from state, but moves are performed in a random order.

        CAUTION: below implementation is not an optimal one, because it needs to firstly materialize all available moves, which causes:
        1. memory issues in case of a big problem
        2. speed issues.
        It is recommended, to overwrite this method and define a generator for each problem separately.
        """
        moves = list(self.available_moves(state))
        return (move for move in sample(moves, len(moves)))

    @ abstractmethod
    def available_moves(self, state: State) -> Generator[Move[State], None, None]:
        """
        Generates available moves from state
        """
