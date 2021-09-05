from genetic_algorithms.models.algorithm import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class HillClimbing(Algorithm):
    def next_state(self, model: Model, state: State) -> State:
        best_state = state
        best_state_cost = model.cost_for(state)
        for move in model.move_generator.available_moves(state):
            new_state = move.make()
            new_state_cost = model.cost_for(new_state)
            if new_state_cost <= best_state_cost:
                (best_state, best_state_cost) = (new_state, new_state_cost)
        return best_state

