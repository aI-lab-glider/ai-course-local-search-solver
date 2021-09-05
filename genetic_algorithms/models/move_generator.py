from abc import ABC, abstractmethod
from genetic_algorithms.problems.base.state import State
from typing import Generic, TypeVar
from typing import Any, Generator
from genetic_algorithms.problems.base.moves import Move
TState = TypeVar("TState")


class MoveGenerator(ABC):
    @abstractmethod
    def random_move(self, state: State) -> Move:
        """
        Generates random move from state
        """

    @abstractmethod
    def available_moves(self, state: State) -> Generator[Move[Any], None, None]:
        """
        Generates available moves from state
        """

