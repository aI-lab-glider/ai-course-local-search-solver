import genetic_algorithms
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Type
from genetic_algorithms.helpers.camel_to_snake import camel_to_snake

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.models.move_generator import MoveGenerator
from dataclasses import dataclass


class Model(ABC):
    """
    Contains all information about problem we are trying to solve.
    """
    problems = {}

    def __init__(self, initial_solution: State, move_generator: MoveGenerator):
        self.initial_solution = initial_solution
        self.move_generator = move_generator
        self.best_state = initial_solution

    def __init_subclass__(cls):
        Model.problems[camel_to_snake(cls.__name__)] = cls

    @staticmethod
    @abstractmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        """
        Available move generation strategis for this model.
        """

    @staticmethod
    @abstractmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str) -> 'Model':
        """
        Creates model from behcmark file
        """

    @abstractmethod
    def cost_for(self, state: State) -> int:
        """
        Calculates costs for passed state
        """

    @classmethod
    def get_path_to_benchmarks(cls) -> Path:
        return Path(genetic_algorithms.__file__).parent/"problems"/camel_to_snake(cls.__name__)/"benchmarks"
