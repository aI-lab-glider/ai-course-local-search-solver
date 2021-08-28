from abc import ABC, abstractmethod
from genetic_algorithms.problems.base.decision_variable import DecisionVariable
from genetic_algorithms.problems.base.state import State


class Move(ABC):
    @abstractmethod
    def make_on(self, state: State, variable: DecisionVariable) -> State:
        """
        Creates a new assigment as a result of this action on assigment
        :param state: current state of a problem
        :param variable: decision variable on which we do want to make a move
        :returns: new state where passed :param variable: has modified value
        """

    def bind_to(self, state: State) -> 'Move':
        """
        Binds move to a given state
        :param state: state to which move will be binded
        """
        return BindedMove(move=self, initial_state=state)


class BindedMove:
    def __init__(self, move: Move, initial_state: State):
        self.unbinded_move = move
        self.initial_state = initial_state

    def make_on(self, variable: DecisionVariable) -> State:
        return self.unbinded_move.make_on(self.initial_state, variable)

    def unmake(self) -> State:
        """
        Unmakes maked move
        """
        # TODO Should it be so? What if we've applied a sequence of actions?
        return self.initial_state
