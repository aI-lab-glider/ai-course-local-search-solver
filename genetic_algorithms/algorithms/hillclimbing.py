from genetic_algorithms.models.algorithm import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.helpers import History
from typing import Tuple

HISTORY_SIZE = 5


class HillClimbing(Algorithm):
    def __init__(self):
        super(HillClimbing, self).__init__()
        self.history = History[int](HISTORY_SIZE)
        self.n_restarts = 0

    def _hill_climbing(self, model: Model, state: State) -> Tuple[State, int]:
        best_state = state
        best_state_cost = model.cost_for(state)
        for move in model.move_generator.available_moves(state):
            new_state = move.make()
            new_state_cost = model.cost_for(new_state)
            if new_state_cost <= best_state_cost:
                (best_state, best_state_cost) = (new_state, new_state_cost)
        return best_state, best_state_cost

    def next_state(self, model: Model, state: State) -> State:
        next_state, next_state_cost = self._hill_climbing(model, state)
        self.history.append(next_state_cost)
        if self._is_extremum(next_state_cost):
            if self.n_restarts > 0:
                next_state = self._restart(model)
                self.n_restarts -= 1
            else:
                self.is_terminated = True
        return next_state

    def _restart(self, model):
        pass

    def _is_extremum(self, cost_to_check: int):
        return (
            all(cost == cost_to_check for cost in self.history)
            and self.history.is_full()
        )
