import local_search
from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum
from typing import Iterable, Type
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.state import State
from local_search.problems.base.move_generator import MoveGenerator
from dataclasses import dataclass

class Goal(Enum):
    MIN = -1
    MAX = 1

class Problem(ABC):
    """
    Contains all information about problem we are trying to solve.
    """
    problems = {}

    def __init__(self, initial_solution: State, move_generator: MoveGenerator):
        self.initial_solution = initial_solution
        self.move_generator = move_generator

    def __init_subclass__(cls):
        Problem.problems[camel_to_snake(cls.__name__)] = cls

    @abstractmethod
    def random_state(self) -> State:
        """
        Generates a random state
        """

    @abstractmethod
    def objective_for(self, state: State) -> int:
        """
        Calculates costs for passed state
        """

    @abstractmethod
    def goal(self) -> Goal:
        """
        Returns the problem goal, i.e. whether we minimize or rather maximize the objective
        """

    def improvement(self, new_state: State, old_state: State) -> int:
        """
        A helper method. Calculates how much the new_state is better than the old_state.
        Takes optimization goal under consideration.
        """
        improvement = self.objective_for(new_state) - self.objective_for(old_state)
        if self.goal() == Goal.MIN:
            improvement *= -1
        return improvement

    @staticmethod
    @abstractmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        """
        Available move generation strategis for this model.
        """

    @staticmethod
    @abstractmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str) -> 'Problem':
        """
        Creates model from behcmark file
        """

    @classmethod
    def get_path_to_benchmarks(cls) -> Path:
        return Path(local_search.__file__).parent / "problems" / camel_to_snake(cls.__name__) / "benchmarks"
