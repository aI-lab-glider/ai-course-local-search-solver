from genetic_algorithms.algorithms.hillclimbing import HillClimbing
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model

N_RANDOM_RESTARTS = 5
N_RANDOM_CHANGES = 5


class HillClimbingWithRandomRestarts(HillClimbing):
    def __init__(self):
        super(HillClimbingWithRandomRestarts, self).__init__()
        self.n_restarts = N_RANDOM_RESTARTS
        self.n_random_changes = N_RANDOM_CHANGES

    def _restart(self, model: Model) -> State:
        initial_state = model.initial_solution

        for i in range(self.n_random_changes):
            initial_state = model.move_generator.random_move(initial_state).make()

        return initial_state
