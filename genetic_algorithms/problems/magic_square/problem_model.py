import math
from pathlib import Path
from genetic_algorithms.problems.base.model import Model
from typing import Generator, List
import random
from genetic_algorithms.problems.magic_square.moves import SwapNumbers
from genetic_algorithms.problems.magic_square.state import MagicSquareState
import numpy as np


class MagicSquareModel(Model):
    def __init__(self, numbers: np.matrix, magic_number: int):
        self._numbers: np.matrix = numbers
        self._magic_number = magic_number
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution)

    @property
    def get_numbers(self):
        return self._numbers

    def _find_initial_solution(self) -> MagicSquareState:
        np.random.shuffle(self._numbers)
        return MagicSquareState(model=self)

    def moves_for(self, state: MagicSquareState) -> Generator[SwapNumbers, None, None]:
        return(SwapNumbers(state, [a, b], [c, d]) for a in range(len(state.numbers)) for b in range(len(state.numbers)) for c in range(len(state.numbers)) for d in range(len(state.numbers)) if d > b or (d == b and c > a))

    def cost_for(self, state: MagicSquareState) -> int:
        row_cost_sum = abs(self._numbers.sum(axis=1) - self._magic_number).sum()
        columnt_cost_sum = abs(self._numbers.sum(axis=0) - self._magic_number).sum()
        left_diagonal_cost = np.trace(self._numbers) - self._magic_number
        right_diagonal_cost = np.trace(np.fliplr(self._numbers)) - self._magic_number
        cost = row_cost_sum + columnt_cost_sum + left_diagonal_cost + right_diagonal_cost
        return cost

    @staticmethod
    def from_benchmark(benchmark_name: str):
        with open(Path.cwd()/"genetic_algorithms"/"problems"/"magic_square"/"benchmarks"/benchmark_name) as benchmark_file:
            magic_number = int(benchmark_file.readline())
            numbers = benchmark_file.readlines()
            list_of_np_matrixes = [np.matrix(numbers[x]) for x in range(len(numbers))]
            output = list_of_np_matrixes[0]
            for i in range(1, len(list_of_np_matrixes)):
                output = np.vstack((output, list_of_np_matrixes[i]))
            return MagicSquareModel(
                numbers=output,
                magic_number=magic_number
            )