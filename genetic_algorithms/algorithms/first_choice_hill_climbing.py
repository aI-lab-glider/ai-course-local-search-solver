from genetic_algorithms.models.algorithm import Algorithm
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.base.model import Model


class FirstChoiceHillClimbing(Algorithm):
    """
    Implementaion of stochastic local search. 

    Stochastic version of hill climbing. Algorithm works, by generating one random move,
    applying it to the state and checking if new state is better. 
    In case if new state is better, then algorithm select it and returns, otherwise, it reverts last move.
    """

    def next_state(self, model: Model, state: State) -> State:
        cost_to_outperform = model.cost_for(state)
        for move in model.move_generator.random_moves(state):
            new_state = move.make()
            new_cost = model.cost_for(new_state)
            if new_cost <= cost_to_outperform:
                return new_state
