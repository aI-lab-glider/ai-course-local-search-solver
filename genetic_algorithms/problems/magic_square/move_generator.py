import random
from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.magic_square.state import MagicSquareState
from genetic_algorithms.problems.magic_square.moves import SwapNumbers
from typing import Generator, Tuple
from itertools import permutations


class MagicSquareMoveGenerator(MoveGenerator):
    def available_moves(self, state: MagicSquareState) -> Generator[SwapNumbers, None, None]:
        return (SwapNumbers(state, (a, b), (c, d))
                for a, b, c, d in permutations(range(len(state.numbers)), 4)
                if d > b or (d == b and c > a))
