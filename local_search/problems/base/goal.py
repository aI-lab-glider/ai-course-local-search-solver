from abc import ABC, abstractmethod
from enum import Enum
from local_search.problems.base.state import State

class GoalType(Enum):
    MIN = -1
    MAX = 1

class Goal(ABC):
    @abstractmethod
    def objective_for(self, state: State) -> int:
        """
        Calculates objective for passed state
        """

    @abstractmethod
    def human_readable_objective_for(self, state: State) -> str:
        """
        Shows human readable objective
        """

    @abstractmethod
    def type(self) -> GoalType:
        """
        Returns the problem goal, i.e. whether we minimize or rather maximize the objective
        """