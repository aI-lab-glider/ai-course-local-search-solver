import random
from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.magic_square.state import MagicSquareState
from genetic_algorithms.problems.magic_square.moves import SwapNumbers
from typing import Generator, Tuple


class MagicSquareMoveGenerator(MoveGenerator):
    def __init__(self, index_1: Tuple[int, int],  index_2 :Tuple[int, int]):
        self.index_1 = index_1
        self.index_2 = index_2

    def _generate_move(self, state: MagicSquareState):
        while True:
            yield SwapNumbers(state, self.index_1, self.index_2)

    def random_moves(self, state: MagicSquareState) -> Generator[SwapNumbers, None, None]:
        return self._generate_move(state)

    def available_moves(self, state: MagicSquareState) -> Generator[SwapNumbers, None, None]:
        return (SwapNumbers(state, (a, b), (c, d)) for a in range(len(state.numbers)) for b in range(len(state.numbers)) for c in range(len(state.numbers)) for d in range(len(state.numbers)) if d > b or (d == b and c > a))
