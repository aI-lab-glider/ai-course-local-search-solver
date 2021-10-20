from dataclasses import dataclass
from local_search.problems.base.state import State
import numpy as np


@dataclass
class MagicSquareState(State):
    numbers: np.ndarray
    magic_number: int

    def __str__(self):
        rows = [" ".join([f'[cyan]{num}[/cyan]' for num in row])
                for row in self.numbers]
        return f"Magic number: {self.magic_number}" + "\n".join(rows)

    def __eq__(self, other):
        if other is None:
            return False
        return self.numbers == other.numbers and self.magic_number == other.magic_number

    def asdict(self):
        return {
            'numbers': self.numbers,
            'magic_number': self.magic_number
        }

    @classmethod
    def from_dict(cls, data):
        numbers = np.array(data['numbers'])
        magic_number = data['magic_number']
        return cls(numbers=numbers, magic_number=magic_number)
