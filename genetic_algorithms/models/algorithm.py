from abc import ABC, abstractmethod
from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class Algorithm(ABC):
    def __init__(self):
        self.is_terminated = False

    @abstractmethod
    def next_state(self, model: Model, state: State) -> State:
        """
        Chooses move to make and returns next state
        """