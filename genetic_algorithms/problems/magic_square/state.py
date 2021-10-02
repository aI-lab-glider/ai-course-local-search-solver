from dataclasses import dataclass
from genetic_algorithms.problems.base.state import State
import numpy as np


@dataclass
class MagicSquareState(State):
    numbers: np.matrix

    def __str__(self):
        rows = [" ".join([f'[cyan]{num}[/cyan]' for num in row])
                for row in self.numbers]
        return "\n".join(rows)
