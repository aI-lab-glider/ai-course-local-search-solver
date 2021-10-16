from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.magic_square.state import MagicSquareState
from local_search.problems.magic_square.moves.swap_numbers import SwapNumbers
from typing import Generator
from itertools import permutations
from abc import ABC
from local_search.helpers.camel_to_snake import camel_to_snake


class MagicSquareMoveGenerator(MoveGenerator, ABC):
    move_generators = {}

    def __init_subclass__(cls):
        MagicSquareMoveGenerator.move_generators[camel_to_snake(cls.__name__)] = cls

    def available_moves(self, state: MagicSquareState) -> Generator[SwapNumbers, None, None]:
        """is it needed there?"""
        return (SwapNumbers(state, (a, b), (c, d))
                for a, b, c, d in permutations(range(len(state.numbers)), 4)
                if d > b or (d == b and c > a))

