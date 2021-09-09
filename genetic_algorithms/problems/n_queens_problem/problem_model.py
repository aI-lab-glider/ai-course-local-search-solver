from typing import Generator, List
from genetic_algorithms.problems.n_queens_problem.state import QueensState
from genetic_algorithms.problems.n_queens_problem.moves import ChangeQueenPosition
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.n_queens_problem.models.queen import Queen


class NQueensModel(Model):
    def __init__(self, queens: List[Queen], column: int):
        self._queens: List[Queen] = queens
        self.n_queens = len(queens)
        self.column = column
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution)

    def _find_initial_solution(self) -> QueensState:
        init_queens = [Queen(row=i, column=i) for i in range(self.n_queens)]
        return QueensState(model=self, queens=init_queens)

    def _count_possible_attacks(self,queen: Queen, state: QueensState) -> int:
        result = 0

        for q in state.queens:
            if queen.row != q.row and queen.column == q.column:
                result += 1
            if queen.row == q.row and queen.column != q.column:
                result += 1

            for j in range(1,self.n_queens):
                if queen.row + j == q.row and queen.column + j == q.column:
                    result += 1
                if queen.row + j == q.row and queen.column - j == q.column:
                    result += 1
                if queen.row - j == q.row and queen.column + j == q.column:
                    result += 1
                if queen.row - j == q.row and queen.column - j == q.column:
                    result += 1

        return result

    def moves_for(self, state: QueensState) -> Generator[ChangeQueenPosition, None, None]:
        return (ChangeQueenPosition(state, row, self.column) for row in range(self.n_queens))

    def cost_for(self, state: QueensState) -> int:
        return sum([self._count_possible_attacks(queen, state) for queen in self._queens])
