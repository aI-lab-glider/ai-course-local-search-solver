import random
from itertools import combinations


from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.traveling_salesman_problem.state import TravelingSalesmanState
from genetic_algorithms.problems.traveling_salesman_problem.moves import SwapEdges
from genetic_algorithms.problems.traveling_salesman_problem.models.edge import Edge
from typing import Generator


class TravelingSalesmanMoveGenerator(MoveGenerator):
    def __init__(self, depot_idx: int):
        self._depot_idx = depot_idx

    def _is_depot_start(self, a: Edge):
        return a.start != self._depot_idx

    def _is_depot_end(self, b: Edge):
        return b.end != self._depot_idx

    def random_move(self, state: TravelingSalesmanState) -> SwapEdges:
        return SwapEdges(state, random.choice(list(state.edges)), random.choice(list(state.edges)))

    def available_moves(self, state: TravelingSalesmanState) -> Generator[SwapEdges, None, None]:
        return (SwapEdges(state, a, b) for a, b in combinations(state.edges, 2)
                if not self._is_depot_start(a) and not self._is_depot_end(b))

