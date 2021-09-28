from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.magic-square.state import MagicSquareState


class SwapNumbers(Move[MagicSquareState]):
    def __init__(self, from_state: MagicSquareStateState, index_1: int, index_2: int):
        super().__init__(from_state)
        (self.index_1, self.index_2) = index_1, index_2

    def make(self) -> MagicSuqareState:
        index_1, index_2 = self.index_1, self.index_2
        numbers = [*self.state.numbers]
        number[index_1], number[index_2] = number[index_2], number[index_1]
        return MagicSuqareState(model=self.state.model, numbers=numbers)
