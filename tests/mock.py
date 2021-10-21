from __future__  import annotations
import random
from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Type, Generator

from local_search.problems import State, Problem
from local_search.problems.base import TProblem, Move
from local_search.problems.base.goal import Goal, GoalType
from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.base.moves import TState


@dataclass
class MockState(State):
    a: int
    b: int

    def __str__(self) -> str:
        return f"{self.a} + {self.b}"

    def __eq__(self, other):
        return isinstance(other, MockState) and self.a == other.a and self.b == other.b

    @staticmethod
    def suboptimal_state(sum: int = 100) -> MockState:
        a = int(0.25 * sum)
        return MockState(a, sum - a)

    @staticmethod
    def optimal_state(goal_type: GoalType, sum: int = 100) -> MockState:
        a = int(0.5 * sum) if goal_type == GoalType.MIN else 0
        return MockState(a, sum - a)


class MockGoal(Goal,ABC):

    def objective_for(self, state: MockState) -> int:
        return state.a ** 2 + state.b ** 2

    def human_readable_objective_for(self, state: MockState) -> str:
        return f"{self.objective_for(state)}"


class MockGoalMax(MockGoal):

    def type(self) -> GoalType:
        return GoalType.MAX


class MockGoalMin(MockGoal):

    def type(self) -> GoalType:
        return GoalType.MIN


@dataclass
class MockMoveGenerator(MoveGenerator):
    sum: int

    def available_moves(self, state: MockState) -> Generator[Move[MockState], None, None]:
        for na in range(max(0, state.a - 2), min(self.sum, state.a + 2)):
            yield MockMove(na, self.sum)


@dataclass
class MockMove(Move):
    new_a: int
    sum: int

    def make(self) -> MockState:
        return MockState(self.new_a, self.sum - self.new_a)


class MockProblem(Problem):
    sum: int

    def __init__(self, sum: int, goal: MockGoal):
        self.sum = sum
        self.goal = goal
        self.move_generator = MockMoveGenerator(self.sum)

    def random_state(self) -> MockState:
        a = random.randrange(self.sum + 1)
        return MockState(a, self.sum - a)

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return ["MockMoveGenerator"]

    @staticmethod
    def get_available_goals() -> Iterable[str]:
        return ["MockGoalMin", "MockGoalMax"]

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str = None, goal_name: str = None,
                       **kwargs) -> MockProblem:
        return MockProblem(100)

    @classmethod
    def from_dict(cls: Type[MockProblem], data) -> MockProblem:
        return MockProblem(100)