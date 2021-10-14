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

    def human_readable_objective_for(self, state: State) -> str:
        return self.goal.human_readable_objective_for(state)

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
    def from_benchmark(benchmark_name: str, move_generator_name: str = None, goal_name: str = None, **kwargs) -> 'Problem':
        """
        Creates model from behcmark file
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

    def asdict(self):
        """
        Creates dictionary with keys same as parameters from __init__ method.
        """
        return {
            'name': camel_to_snake(type(self).__name__),
            'goal_name': camel_to_snake(type(self.goal).__name__),
            'move_generator_name': camel_to_snake(type(self.move_generator).__name__),
        }

    @classmethod
    def validate_data(cls, data):
        """
        Validates if data contains all params from class signature.
        """
        params = set(signature(cls).parameters.keys())
        missing_params = params - set(data.keys())
        if missing_params:
            raise ValueError(
                f'Cannot create {cls.__name__} from passed dict. Missing params are: {",".join(missing_params)}')

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[TProblem], data) -> TProblem:
        """
        Creates problem from dict representation.
        """
        name = data['name']
        problem_type = cls.problems[name]
        problem_type.validate_data(data)
        del data['name']
        return problem_type.from_dict(data)
