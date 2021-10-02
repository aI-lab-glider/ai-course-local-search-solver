from pathlib import Path
import genetic_algorithms
from genetic_algorithms.problems.base.model import Model
from typing import Generator, List
from genetic_algorithms.problems.magic_square.moves import SwapNumbers
from genetic_algorithms.problems.magic_square.state import MagicSquareState
from genetic_algorithms.problems.magic_square.move_generator import MagicSquareMoveGenerator
import numpy as np


class MagicSquareProblem(Model):
    def __init__(self, numbers: np.ndarray, magic_number: int, move_generator: MagicSquareMoveGenerator):
        self._numbers = numbers
        self._magic_number = magic_number
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution, move_generator)

    @property
    def get_numbers(self):
        return self._numbers

    def _find_initial_solution(self) -> MagicSquareState:
        np.random.shuffle(self._numbers)
        return MagicSquareState(model=self, numbers=self._numbers)

    def cost_for(self, state: MagicSquareState) -> int:
        row_cost_sum = abs(self._numbers.sum(
            axis=1) - self._magic_number).sum()
        columnt_cost_sum = abs(self._numbers.sum(
            axis=0) - self._magic_number).sum()
        left_diagonal_cost = np.trace(self._numbers) - self._magic_number
        right_diagonal_cost = np.trace(
            np.fliplr(self._numbers)) - self._magic_number
        cost = row_cost_sum + columnt_cost_sum + \
            left_diagonal_cost + right_diagonal_cost
        return cost

    @staticmethod
    def from_benchmark(benchmark_name: str):
        with open(Path(genetic_algorithms.__file__).parent/"problems"/"magic_square"/"benchmarks"/benchmark_name) as benchmark_file:
            magic_number = int(benchmark_file.readline())
            numbers = [list(map(int, line.split(',')))
                       for line in benchmark_file.readlines()]
            numbers = np.array(numbers)
            return MagicSquareProblem(
                numbers=numbers,
                magic_number=magic_number,
                move_generator=MagicSquareMoveGenerator()
            )
