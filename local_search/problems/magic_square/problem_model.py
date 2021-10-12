from pathlib import Path
import local_search
from local_search.problems.base.problem import Problem
from typing import Generator, List
from local_search.problems.magic_square.moves import SwapNumbers
from local_search.problems.magic_square.state import MagicSquareState
from local_search.problems.magic_square.move_generator import MagicSquareMoveGenerator
from local_search.problems.magic_square.goals.goal import MagicSquareGoal
import numpy as np


class MagicSquareProblem(Problem):
    def __init__(self, numbers: np.ndarray, magic_number: int, move_generator: MagicSquareMoveGenerator, goal: MagicSquareGoal):
        self._numbers = numbers
        self._magic_number = magic_number
        self.goal = goal
        initial_solution = self.random_state()
        super().__init__(initial_solution, move_generator, goal)

    @property
    def get_numbers(self):
        return self._numbers

    def random_state(self) -> MagicSquareState:
        np.random.shuffle(self._numbers)
        return MagicSquareState(numbers=np.asmatrix(self._numbers), magic_number=self._magic_number)

    @staticmethod
    def from_benchmark(benchmark_name: str, move_generator_name: str = None, goal_name: str = None):
        with open(Path(local_search.__file__).parent/"problems"/"magic_square"/"benchmarks"/benchmark_name) as benchmark_file:
            magic_number = int(benchmark_file.readline())
            numbers = [list(map(int, line.split(',')))
                       for line in benchmark_file.readlines()]
            numbers = np.array(numbers)
            return MagicSquareProblem(
                numbers=numbers,
                magic_number=magic_number,
                move_generator=MagicSquareMoveGenerator(),
                goal=MagicSquareGoal()
            )

