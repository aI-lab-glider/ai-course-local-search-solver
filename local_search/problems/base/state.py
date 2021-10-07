from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class State(ABC):

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representing a problem.
        """

    @abstractmethod
    def __eq__(self, other):
        """
        Compares current states to another state.
        """
