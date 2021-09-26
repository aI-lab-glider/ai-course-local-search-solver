import random
from itertools import combinations

from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.traveling_salesman_problem.state import TravelingSalesmanState
from genetic_algorithms.problems.traveling_salesman_problem.moves import SwapEdges
from typing import Generator


class TravelingSalesmanMoveGenerator(MoveGenerator):
    def __init__(self, depot_idx: int):
        self._depot_idx = depot_idx

    def _depot_start(self, move: SwapEdges):
        return move.a.start != self._depot_idx

    def _depot_end(self, move: SwapEdges):
        return move.b.end != self._depot_idx

    def _satisfies_constraints(self, move: SwapEdges):
        constraints = [self._depot_start, self._depot_end]
        return all([constraint(move) for constraint in constraints])

    def _generate_move(self, state: TravelingSalesmanState):
        new_move = lambda: SwapEdges(state, random.choice(list(state.edges)), random.choice(list(state.edges)))
        while True:
            random_move = new_move()
            if self._satisfies_constraints(random_move):
                yield random_move

    def random_moves(self, state: TravelingSalesmanState) -> Generator[SwapEdges, None, None]:
        return self._generate_move(state)

    def available_moves(self, state: TravelingSalesmanState) -> Generator[SwapEdges, None, None]:
        return (SwapEdges(state, a, b) for a, b in combinations(state.edges, 2)
                if self._satisfies_constraints(SwapEdges(state, a, b)))

