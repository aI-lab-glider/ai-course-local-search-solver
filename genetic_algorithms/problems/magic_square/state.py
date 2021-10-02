from dataclasses import dataclass
from typing import Iterable, List
from genetic_algorithms.problems.base.state import State
import numpy as np


@dataclass
class MagicSquareState(State):
    numbers: np.matrix

    def __str__(self):
        return self.numbers
