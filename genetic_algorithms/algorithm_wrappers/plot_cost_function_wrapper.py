from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.algorithm_wrappers.algorithm_wrapper import AlgorithmWrapper


class CostPrinterWrapper(AlgorithmWrapper):
    def _perform_side_effects(self, model: Model, state: State):
        new_cost = model.cost_for(state)
        print('New cost received: ', new_cost)
