from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.n_queens_problem.state import QueensState


class ChangeQueenPosition(Move[QueensState]):
    def __init__(self, from_state: QueensState, row: int, column: int):
        super().__init__(from_state)
        (self.row, self.column) = row, column

    def make(self) -> QueensState:
        new_configuration = [*self.state.queens]
        new_configuration[self.column].row = self.row
        return QueensState(model=self.state.model, queens=new_configuration)
