import math
from genetic_algorithms.models.algorithm import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.helpers import History
from typing import Tuple
import random


HISTORY_SIZE = 5


class SimulatedAnnealing(Algorithm):
    def __init__(self):
        super(SimulatedAnnealing, self).__init__()
        self.history = History[int](HISTORY_SIZE)
        # how to set temperature ???
        self.temperature = 100

    def _simulated_annealing(self, model: Model, state: State) -> Tuple[State, int]:
        best_state = state
        best_state_cost = model.cost_for(state)
        move_iteration_number = 0
        for move in model.move_generator.available_moves(state):
            new_state = move.make()
            new_state_cost = model.cost_for(new_state)
            if new_state_cost <= best_state_cost:
                (best_state, best_state_cost) = (new_state, new_state_cost)
            else:
                # difference between new state cost and current state cost
                diff = new_state_cost - best_state_cost
                # calculate temperature for current iteration
                self.temperature = self.temperature / float(move_iteration_number + 1)
                # calculate value of metropolis acceptance criterion
                criterion_value = math.exp(-diff/self.temperature)
                if random.random() < criterion_value:
                    (best_state, best_state_cost) = (new_state, new_state_cost)
            move_iteration_number += 1
        return best_state, best_state_cost

    def next_state(self, model: Model, state: State) -> State:
        next_state, next_state_cost = self._simulated_annealing(model, state)
        self.history.append(next_state_cost)
        if self._is_not_moving_forward(next_state_cost):
            self.is_terminated = True
        return next_state


    def _is_not_moving_forward(self, cost_to_check: int):
        return (
            all(cost == cost_to_check for cost in self.history)
            and self.history.is_full()
        )