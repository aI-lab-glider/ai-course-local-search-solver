from abc import ABC, abstractmethod
from typing import Any, Generator

from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.base.state import State


class Model(ABC):
    def __init__(self, initial_solution: State):
        self.initial_solution = initial_solution

    @abstractmethod
    def moves_for(self, state: State) -> Generator[Move[Any], None, None]:
        """
        Returns actions that could be done on problem to generate neighboorhood
        """

    @abstractmethod
    def cost_for(self, state: State) -> int:
        """
        Calculates costs for passed state
        """
