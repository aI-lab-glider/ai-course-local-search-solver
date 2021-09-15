from genetic_algorithms.algorithms.hillclimbing import HillClimbing
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model

N_RESTARTS = 5
N_RANDOM_CHANGES = 3


class IteratedLocalSearch(HillClimbing):
    def __init__(self):
        super(IteratedLocalSearch, self).__init__()
        self.n_restarts = N_RESTARTS
        self.n_random_changes = N_RANDOM_CHANGES

    def _restart(self, model: Model) -> State:
        initial_state = model.best_state

        for i in range(self.n_random_changes):
            initial_state = model.move_generator.random_move(initial_state).make()

        return initial_state
