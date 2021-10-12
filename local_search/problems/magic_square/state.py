from dataclasses import dataclass
from local_search.problems.base.state import State
import numpy as np


@dataclass
class MagicSquareState(State):
    numbers: np.matrix
    magic_number: int

    def __str__(self):
        rows = [" ".join([f'[cyan]{num}[/cyan]' for num in row])
                for row in self.numbers]
        return "\n".join(rows)

    def __eq__(self, other):
        if self.numbers == other.numbers:
            return True
        return False

    def asdict(self):
        return {i: self.numbers.flatten()[i] for i in range(len(self.numbers))}

    def from_dict(self, data) -> 'State':
        x = np.sqrt(len(data))
        numbers = np.array(data.values())
        numbers = np.asmatrix(np.reshape(numbers, (x, x)))
        return MagicSquareState(numbers=numbers)



