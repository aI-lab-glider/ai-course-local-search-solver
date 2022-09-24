from __future__ import annotations

import random
from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Type, Generator

from local_search.problems import State, Problem
from local_search.problems.base import Move
from local_search.problems.base.goal import Goal, GoalType
from local_search.problems.base.move_generator import MoveGenerator


@dataclass
class SumProblemState(State):
    a: int
    b: int

    def __str__(self) -> str:
        return f"{self.a} + {self.b}"

    def __eq__(self, other):
        return isinstance(other, SumProblemState) and self.a == other.a and self.b == other.b

    @staticmethod
    def suboptimal_state(sum: int = 100) -> SumProblemState:
        a = int(0.25 * sum)
        return SumProblemState(a, sum - a)

    @staticmethod
    def optimal_state(goal_type: GoalType, sum: int = 100) -> SumProblemState:
        a = int(0.5 * sum) if goal_type == GoalType.MIN else 0
        return SumProblemState(a, sum - a)


class SumProblemGoal(Goal, ABC):

    def objective_for(self, state: SumProblemState) -> int:
        return state.a ** 2 + state.b ** 2

    def human_readable_objective_for(self, state: SumProblemState) -> str:
        return f"{self.objective_for(state)}"


class Maximize(SumProblemGoal):

    def type(self) -> GoalType:
        return GoalType.MAX


class Minimize(SumProblemGoal):

    def type(self) -> GoalType:
        return GoalType.MIN


@dataclass
class SumProblemMoveGenerator(MoveGenerator):
    sum: int

    def available_moves(self, state: SumProblemState) -> Generator[Move[SumProblemState], None, None]:
        for na in range(max(0, state.a - 2), min(self.sum, state.a + 2)):
            yield SumProblemMove(na, self.sum)


@dataclass
class SumProblemMove(Move):
    new_a: int
    sum: int

    def make(self) -> SumProblemState:
        return SumProblemState(self.new_a, self.sum - self.new_a)


class SumProblem(Problem):
    """
    Demonstration of a simple problem, where the goal is to decompose :param sum: into components.
    """
    def __init__(self, sum: int, goal: SumProblemGoal):
        self.sum = sum
        self.goal = goal
        self.move_generator = SumProblemMoveGenerator(self.sum)

    def random_state(self) -> SumProblemState:
        a = random.randrange(self.sum + 1)
        return SumProblemState(a, self.sum - a)

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return ["MockMoveGenerator"]

    @staticmethod
    def get_available_goals() -> Iterable[str]:
        return ["MockGoalMin", "MockGoalMax"]

    @staticmethod
    def from_benchmark(**kwargs) -> SumProblem:
        raise NotImplementedError(
            f"{SumProblem.__name__} cannot be created from benchmark")

    @classmethod
    def from_dict(cls: Type[SumProblem], **kwargs) -> SumProblem:
        raise NotImplementedError(
            f"{SumProblem.__name__} cannot be created from dict")

    def next_states_from(self, state: SumProblemState) -> Iterable[SumProblemState]:
        for move in self.move_generator.available_moves(state):
            yield move.make()

