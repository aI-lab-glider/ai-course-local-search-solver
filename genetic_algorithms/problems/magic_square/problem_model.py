from genetic_algorithms.problems.base.model import Model
from typing import Generator, List
import random


class MagicSquareModel(Model):
    def __init__(self, numbers: List[Point], magic_number: int):
        self._numbers: List[Point] = numbers
        self._magic_number = magic_number
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution)

    @property
    def get_numbers(self):
        return self._numbers

    def _find_initial_solution(self) -> MagicSquareState:
        shuffled_list = random.shuffle(self._numbers)
        return MagicSquareState(model=self, shuffled_number_list=shuffled_list)

    @staticmethod
    def moves_for(self, state: MagicSquareState) -> Generator[SwapNumbers, None, None]:
        indexes_to_change_list = []
        for i in range(len(state.numbers)):
            for j in range(len(state.numbers)):
                if j>i:
                    indexes_to_change_list.append((i, j))
        return(SwapNumbers(state, a, b) for a, b in indexes_to_change_list)


    def cost_for(self, state: MagicSquareState) -> int:
        size_of_square = sqrt(len(self._numbers))
        cost = 0
        for i in range(size_of_square):
            curr_row = [self._numbers[j] for j in xrange(i*size_of_square, (i*size_of_square)+1, 1)]
            curr_col = [self._numbers[j] for j in xrange(i, len(self._numbers), size_of_square)]
            current_row_sum = sum(curr_row)
            current_column_sum = sum(curr_col)
            cost += abs(current_column_sum-self._magic_number)
            cost += abs(current_row_sum-self._magic_number)
        left_diagonal_sum = 0
        right_diagonal_sum = 0
        for i in range(size_of_square):
            left_diagonal_sum += self._numbers[i*(size_of_square+1)]
            right_diagonal_sum += self._numbers[(size_of_square-1)+i*(size_of_square-1)]
        cost += abs(left_diagonal_sum-self._magic_number)
        cost += abs(right_diagonal_sum-self._magic_number)
        return cost

    @staticmethod
    def from_benchmark(benchmark_name: str):
        with open(Path.cwd()/"genetic_algorithms"/"problems"/"magic-square"/"benchmarks"/benchmark_name) as benchmark_file:
            magic_number = int(benchmark_file.readline())
            numbers = str(benchmark_file.readline())
            numbers = numbers.split()
            numbers = [int(x) for x in numbers]
            return MagicSquareModel(
                numbers=numbers,
                magic_number=magic_number
            )