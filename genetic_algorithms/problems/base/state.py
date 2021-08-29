from abc import ABC, abstractmethod
from typing import List
from genetic_algorithms.problems.base.decision_variable import DecisionVariable
from genetic_algorithms.problems.base.model import Model


class State(ABC):
    def __init__(self, model: Model, variables: List[DecisionVariable]):
        self.original_model = model
        self.decision_variables = variables

    def with_replaced(self, variable: DecisionVariable) -> 'State':
        """
        Returns new :class State: with replaced decision variable
        """
        new_decision_vars = [*self.decision_vars]
        new_decision_vars[variable.idx] = variable
        return State(self.original_model, new_decision_vars)

    @abstractmethod
    def print(self):
        """
        Prints a solution to the problem
        """
