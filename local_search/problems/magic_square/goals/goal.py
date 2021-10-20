from local_search.problems.base.goal import GoalType, Goal
from local_search.problems.magic_square.state import MagicSquareState
import numpy as np


class MagicSquareGoal(Goal):

    def objective_for(self, state: MagicSquareState) -> int:
        row_cost_sum = abs(state.numbers.sum(
            axis=1) - state.magic_number).sum()
        column_cost_sum = abs(state.numbers.sum(
            axis=0) - state.magic_number).sum()
        left_diagonal_cost = np.trace(state.numbers) - state.magic_number
        right_diagonal_cost = np.trace(
            np.fliplr(state.numbers)) - state.magic_number
        return row_cost_sum + column_cost_sum + left_diagonal_cost + right_diagonal_cost

    def human_readable_objective_for(self, state: MagicSquareState) -> str:
        return f'{self.objective_for(state)} broken constraints'

    def type(self) -> GoalType:
        return GoalType.MIN
