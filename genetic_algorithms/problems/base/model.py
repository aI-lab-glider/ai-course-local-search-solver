from abc import ABC, abstractmethod
from genetic_algorithms.problems.base.decision_variable import DecisionVariable
from genetic_algorithms.problems.base.moves import Move
from typing import List
from genetic_algorithms.problems.base.state import State
from dataclasses import dataclass


@dataclass
class Violation:
    cost: int
    decision_variable: DecisionVariable


class Model(ABC):
    def __init__(self, initial_solution: State):
        self.initial_solution = initial_solution

    @property
    @abstractmethod
    def valid_moves(self) -> List[Move]:
        """
        Returns actions that could be done on problem to generate neighboorhood
        """

    @abstractmethod
    def find_violations_in(self, state: State) -> List[Violation]:
        """
        Returns violations present in state
        """

    @abstractmethod
    def cost_for(self, state: State) -> int:
        """
        Calculates costs for passed state
        """
