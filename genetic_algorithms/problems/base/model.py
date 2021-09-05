from abc import ABC, abstractmethod
from typing import Any, Generator

from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.models.move_generator import MoveGenerator


class Model(ABC):
    def __init__(self, initial_solution: State, move_generator: MoveGenerator):
        self.initial_solution = initial_solution
        self.move_generator = move_generator

    @abstractmethod
    def moves_for(self, state: State) -> Generator[Move[Any], None, None]:
        """
        Returns actions that could be done on problem to generate neighborhood
        """

    @abstractmethod
    def cost_for(self, state: State) -> int:
        """
        Calculates costs for passed state
        """
