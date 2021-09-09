from dataclasses import dataclass
from typing import List

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.n_queens_problem.models.queen import Queen


@dataclass
class QueensState(State):
    queens: List[Queen]

    def __str__(self):
        return " ".join([f"({q.row}, {q.column})" for q in self.queens])
