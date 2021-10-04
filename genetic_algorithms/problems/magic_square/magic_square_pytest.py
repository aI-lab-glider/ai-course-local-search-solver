import pytest
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.magic_square.state import MagicSquareState
from genetic_algorithms.problems.magic_square.moves import SwapNumbers
from genetic_algorithms.problems.magic_square.problem_model import MagicSquareModel
from genetic_algorithms.problems.magic_square.move_generator import MagicSquareMoveGenerator


class TestCostFunctionCalc:

    def test_cost_function(self):
        magic_number = 15
        move_generator = MagicSquareMoveGenerator
        model = MagicSquareModel(MagicSquareModel.from_benchmark("ms_1"), magic_number, move_generator)
        current_state = MagicSquareState(model=model, numbers=model.get_numbers)
        result = model.cost_for(current_state)
        assert result == 16