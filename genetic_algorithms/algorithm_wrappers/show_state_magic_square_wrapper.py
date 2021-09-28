import math
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper


class MagicSquarePrinterWrapper(AlgorithmWrapper):
    def _perform_side_effects(self, model: Model, state: State):
        numbers = state.__str__()
        for i in range(len(numbers)):
            print("|", numbers[i], end=" ")
            if (i + 1) % math.sqrt(len(numbers)) == 0:
                print("|")
                print("-------------")
