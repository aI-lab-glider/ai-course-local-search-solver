from pathlib import Path
import local_search
from typing import Iterable
from local_search.problems.base.problem import Problem
from local_search.problems.magic_square.state import MagicSquareState
from local_search.problems.magic_square.moves.move_generator import MagicSquareMoveGenerator
from local_search.problems.magic_square.goals.goal import MagicSquareGoal
import numpy as np


class MagicSquareProblem(Problem):
    def __init__(self, initial_solution: MagicSquareState, move_generator: MagicSquareMoveGenerator, goal: MagicSquareGoal):
        super().__init__(initial_solution, move_generator, goal)

    def random_state(self) -> MagicSquareState:
        np.random.shuffle(self.initial_state.numbers)
        return MagicSquareState(numbers=self.initial_state.numbers, magic_number=self.initial_state.magic_number)

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return MagicSquareMoveGenerator.move_generators.keys()

    @staticmethod
    def get_available_goals() -> Iterable[str]:
        return MagicSquareGoal.goals.keys()

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str = None, goal_name: str = None):
        with open(Path(local_search.__file__).parent/"problems"/"magic_square"/"benchmarks"/benchmark_name) as benchmark_file:
            magic_number = int(benchmark_file.readline())
            numbers = [list(map(int, line.split(',')))
                       for line in benchmark_file.readlines()]
            numbers = np.array(numbers)
            initial_state = MagicSquareState(numbers=numbers, magic_number=magic_number)
            return MagicSquareProblem(
                initial_solution=initial_state,
                move_generator=MagicSquareMoveGenerator(),
                goal=MagicSquareGoal()
            )

    @classmethod
    def from_dict(cls, data):
        """ ??? """
        return cls(**data)

    @classmethod
    def from_solution(cls, solution_name: str):
        return cls.from_benchmark(solution_name)


