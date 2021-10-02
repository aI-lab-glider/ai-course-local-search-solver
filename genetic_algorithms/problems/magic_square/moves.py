from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.magic_square.state import MagicSquareState
from typing import Tuple
from copy import deepcopy


class SwapNumbers(Move[MagicSquareState]):
    def __init__(self, from_state: MagicSquareState, index_1: Tuple[int, int], index_2: Tuple[int, int]):
        super().__init__(from_state)
        (self.index_1, self.index_2) = index_1, index_2

    def make(self) -> MagicSquareState:
        index_1, index_2 = self.index_1, self.index_2
        numbers = deepcopy(self.state.numbers)
        numbers[index_1], numbers[index_2] = numbers[index_2], numbers[index_1]
        return MagicSquareState(model=self.state.model, numbers=numbers)
