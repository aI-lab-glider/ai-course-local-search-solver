from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union
from local_search.algorithms.algorithm_config import DEFAULT_CONFIG, AlgorithmConfig
from local_search.problems.base import State
from local_search.problems.base.problem import Problem


@dataclass
class Algorithm(ABC):
    best_obj: Union[float, None] = None
    best_state: Union[State, None] = None
    steps_from_last_state_update: int = 0
    config: AlgorithmConfig = DEFAULT_CONFIG

    @abstractmethod
    def next_state(self, model: Problem, state: State) -> Union[State, None]:
        """
        Returns next state that could be reached from the current state.
        """

    @abstractmethod
    def escape_local_optimum(self, model: Problem, state: State, best_state: State) -> Union[State, None]:
        """
        Asks algorithm to escape from the local minimum if it's possible
        """
