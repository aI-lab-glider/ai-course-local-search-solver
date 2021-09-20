from abc import ABC, abstractmethod

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.models.move_generator import MoveGenerator


class Model(ABC):
    """
    Contains all information about problem we are trying to solve.
    """

    def __init__(self, initial_solution: State, move_generator: MoveGenerator):
        self.initial_solution = initial_solution
        self.move_generator = move_generator
        self.best_state = initial_solution

    @abstractmethod
    def cost_for(self, state: State) -> int:
        """
        Calculates costs for passed state
        """
