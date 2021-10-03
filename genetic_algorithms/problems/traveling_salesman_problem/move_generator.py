from genetic_algorithms.helpers.camel_to_snake import camel_to_snake
import random
from itertools import permutations

from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.traveling_salesman_problem.state import TravelingSalesmanState
from genetic_algorithms.problems.traveling_salesman_problem.moves import SwapEdges
from typing import Generator


class TravelingSalesmanMoveGenerator(MoveGenerator):
    """
    Base class for move generators for traveling salesman problem
    """
    move_generators = {}

    def __init__(self, depot_idx: int):
        self._depot_idx = depot_idx

    def __init_subclass__(cls):
        TravelingSalesmanMoveGenerator.move_generators[camel_to_snake(
            cls.__name__)] = cls


class TwoOpt(TravelingSalesmanMoveGenerator):

    def _is_depot_start(self, move: SwapEdges):
        new_state = move.make()
        return new_state.route[0] == self._depot_idx

    def _is_depot_end(self, move: SwapEdges):
        new_state = move.make()
        return new_state.route[-1] == self._depot_idx

    def _satisfies_constraints(self, move: SwapEdges):
        constraints = [self._is_depot_start, self._is_depot_end]
        return all([constraint(move) for constraint in constraints])

    def _generate_move(self, state: TravelingSalesmanState):
        def new_move(): return SwapEdges(state, random.choice(
            list(state.edges)), random.choice(list(state.edges)))
        while True:
            random_move = new_move()
            if self._satisfies_constraints(random_move):
                yield random_move

    def random_moves(self, state: TravelingSalesmanState) -> Generator[SwapEdges, None, None]:
        return self._generate_move(state)

    def available_moves(self, state: TravelingSalesmanState) -> Generator[SwapEdges, None, None]:
        # TODO Add tests
        return (SwapEdges(state, a, b) for a, b in permutations(state.edges, 2)
                if self._satisfies_constraints(SwapEdges(state, a, b)))


# TODO
# ADD 3-opt
