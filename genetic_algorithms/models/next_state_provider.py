from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union
from genetic_algorithms.problems.base import State
from genetic_algorithms.problems.base.model import Model


@dataclass
class Algorithm(ABC):
    best_cost: Union[float, None] = None
    best_state: Union[State, None] = None
    steps_from_last_state_update: int = 0
    
    @abstractmethod
    def next_state(self, model: Model, state: State) -> Union[State, None]:
        """
        Returns next state that could be reaced from the current state.
        """
    