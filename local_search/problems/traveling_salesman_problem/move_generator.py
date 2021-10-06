from local_search.helpers.camel_to_snake import camel_to_snake
import random
from itertools import permutations

from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.base.moves import Move
from local_search.problems.traveling_salesman_problem.state import TravelingSalesmanState
from local_search.problems.traveling_salesman_problem.moves import SwapThreeEdges, SwapTwoEdges
from typing import Generator, Type, Union


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

    def _is_depot_start(self, move: Move[TravelingSalesmanState]):
        new_state = move.make()
        return new_state.route[0] == self._depot_idx

    def _is_depot_end(self, move: Move[TravelingSalesmanState]):
        new_state = move.make()
        return new_state.route[-1] == self._depot_idx

    def _satisfies_constraints(self, move: Move[TravelingSalesmanState]):
        constraints = [self._is_depot_start, self._is_depot_end]
        return all([constraint(move) for constraint in constraints])


class KOpt(TravelingSalesmanMoveGenerator):
    def __init__(self, k, move: Type[Move[TravelingSalesmanState]], **kwargs):
        self.k = k
        self.move = move
        super().__init__(**kwargs)

    def random_moves(self, state: TravelingSalesmanState) -> Generator[Move[TravelingSalesmanState], None, None]:
        # TODO Test: should not remove points from state :)
        # TODO Test: should be unique points
        # TODO Add random.seed
        def new_move() -> Move[TravelingSalesmanState]:
            edges = list(state.edges)
            return self.move(state, *random.sample(edges, self.k))
        while True:
            random_move = new_move()
            if self._satisfies_constraints(random_move):
                yield random_move

    def available_moves(self, state: TravelingSalesmanState) -> Generator[Move[TravelingSalesmanState], None, None]:
        # TODO Add tests
        # TODO consider direction in permutation
        # TODO points dissapear from state. Prevent loops
        return (self.move(state, *edges) for edges in permutations(state.edges, self.k)
                if self._satisfies_constraints(self.move(state, *edges)))


class TwoOpt(KOpt):
    def __init__(self, depot_idx):
        super().__init__(2, SwapTwoEdges, depot_idx=depot_idx)


class ThreeOpt(KOpt):
    def __init__(self, depot_idx):
        super().__init__(3, SwapThreeEdges, depot_idx=depot_idx)

# TODO
# TSP neingbour
#
