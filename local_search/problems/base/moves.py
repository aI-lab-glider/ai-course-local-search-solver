from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from copy import deepcopy


TState = TypeVar("TState")


class Move(ABC, Generic[TState]):
    def __init__(self, from_state: TState):
        self.state = from_state

    @abstractmethod
    def make(self) -> TState:
        """
        Creates a new state as a result of this action on state
        :param state: current state of a problem
        :param variable: decision variable on which we do want to make a move
        :returns: new state where passed :param variable: has modified value
        """
