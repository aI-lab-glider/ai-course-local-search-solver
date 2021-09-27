from abc import ABC, abstractmethod
from typing import Union
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class NextStateProvider(ABC):
    @abstractmethod
    def next_state(self, model: Model, state: State) -> Union[State, None]:
        """
        Returns next state that could be reaced from the current state.
        """
