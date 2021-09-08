from dataclasses import dataclass
from typing import Iterable, List

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.traveling_salesman_problem.models.edge import \
    Edge


@dataclass
class MagicSquareState(State):
    numbers: List[int]

    def __str__(self):
        print(self.numbers)
        return self.numbers