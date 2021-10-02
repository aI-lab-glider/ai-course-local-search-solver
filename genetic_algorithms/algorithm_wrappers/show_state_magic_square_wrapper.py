import math
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper
import numpy as np
from rich.console import Console
from rich.table import Table
from rich import box


class MagicSquarePrinterWrapper(AlgorithmWrapper):
    def _perform_side_effects(self, model: Model, state: State):
        numbers = state.__str__()
        numbers = numbers.tolist()
        table = Table(title="Current magic-square", show_header=False, show_lines=True, box=box.DOUBLE)
        for row in numbers:
            row = [str(element) for element in row]
            table.add_row(*row)

        console = Console()
        console.print(table)
