from itertools import chain
import local_search
from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum
from typing import Dict, Iterable, Type, TypeVar
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.goal import Goal
from local_search.problems.base.state import State
from local_search.problems.base.move_generator import MoveGenerator
from dataclasses import dataclass
from inspect import getmro, signature

TProblem = TypeVar("TProblem", bound='Problem')


class Problem(ABC):
    """
    Contains all information about problem we are trying to solve.
    """
    problems: Dict[str, Type['Problem']] = {}

    def __init__(self, initial_solution: State, move_generator: MoveGenerator, goal: Goal):
        self.initial_state = initial_solution
        self.move_generator = move_generator
        self.goal = goal

    def __init_subclass__(cls):
        Problem.problems[camel_to_snake(cls.__name__)] = cls

    @abstractmethod
    def random_state(self) -> State:
        """
        Generates a random state
        """

    def objective_for(self, state: State) -> int:
        """
        Just a helper proxy method
        """
        return self.goal.objective_for(state)

    def improvement(self, new_state: State, old_state: State) -> int:
        """
        A helper method. Calculates how much the new_state is better than the old_state.
        Takes optimization goal under consideration.
        """
        improvement = self.objective_for(
            new_state) - self.objective_for(old_state)
        return improvement * self.goal.type().value

    @staticmethod
    @abstractmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        """
        Available move generation strategies for this model.
        """

    @staticmethod
    @abstractmethod
    def get_available_goals() -> Iterable[str]:
        """
        Available goals for this model.
        """

    @staticmethod
    @abstractmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str = None, goal_name: str = None) -> 'Problem':
        """
        Creates model from behcmark file
        """

    @classmethod
    @abstractmethod
    def from_solution(cls, problem_name: str) -> 'Problem':
        """
        Creates model from solution file
        """

    @classmethod
    def get_path_to_module(cls) -> Path:
        return Path(local_search.__file__).parent / "problems" / camel_to_snake(cls.__name__)

    @classmethod
    def get_path_to_benchmarks(cls) -> Path:
        return cls.get_path_to_module() / "benchmarks"

    @classmethod
    def get_path_to_solutions(cls) -> Path:
        return cls.get_path_to_module() / "expected_solutions"

    @abstractmethod
    def asdict():
        """
        Creates dictionary with keys same as parameters from __init__ method.
        """

    @classmethod
    def from_dict(cls: Type[TProblem], data) -> TProblem:
        """
        Creates problem representation as a dict.
        """
        params = set(chain(signature(method).parameters.keys()
                     for method in getmro(cls)))
        missing_params = set(data.keys()) - params
        if missing_params:
            raise ValueError(
                f'Cannot create {cls.__name__} from passed dict. Missing params are: {",".join(missing_params)}')
        return cls(**data)
