from functools import reduce
from genetic_algorithms.problems.traveling_salesman_problem.models.edge import Edge
from itertools import combinations
from pathlib import Path
from typing import Generator, List
import genetic_algorithms

from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.traveling_salesman_problem.models.point import \
    Point
from genetic_algorithms.problems.traveling_salesman_problem.models.salesman import \
    Salesman
from genetic_algorithms.problems.traveling_salesman_problem.moves import \
    SwapEdges
from genetic_algorithms.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState
from genetic_algorithms.problems.traveling_salesman_problem.move_generator import \
    TravelingSalesmanMoveGenerator


class TravelingSalesmanModel(Model):
    def __init__(self, points: List[Point], depot_idx: int):
        self._points: List[Point] = points
        self._depot_idx = depot_idx
        initial_solution = self._find_initial_solution()
        move_generator = TravelingSalesmanMoveGenerator(depot_idx)
        super().__init__(initial_solution, move_generator)

    @property
    def points(self):
        return self._points

    def _find_initial_solution(self) -> TravelingSalesmanState:
        naive_circle = list(
            range(0, len(self._points))) + [self._depot_idx]
        return TravelingSalesmanState(model=self, route=naive_circle)

    def moves_for(self, state: TravelingSalesmanState) -> Generator[SwapEdges, None, None]:
        def is_depot_start(a: Edge):
            return a.start != self._depot_idx

        def is_depot_end(b: Edge):
            return b.end != self._depot_idx
        return (SwapEdges(state, a, b) for a, b in combinations(state.edges, 2) if not is_depot_start(a) and not is_depot_end(b))

    def cost_for(self, state: TravelingSalesmanState) -> int:
        route = [self._points[i]
                 for i in state.route if i != self._depot_idx]
        depot = self._points[self._depot_idx]

        salesman_after_going_through_route = reduce(lambda salesman, new_point: salesman.walk_to(new_point),
                                                    route, Salesman.from_point(
            depot))
        return int(salesman_after_going_through_route.walk_to(depot).walked_distance)

    @staticmethod
    def from_benchmark(benchmark_name: str):
        with open(Path(genetic_algorithms.__file__).parent/"problems"/"traveling_salesman_problem"/"benchmarks"/benchmark_name) as benchmark_file:
            depot_idx = int(benchmark_file.readline())

            def line_to_point(line: str):
                (x, y) = map(int, line.split(sep=' '))
                return Point(x, y)
            points = map(line_to_point, [line for line in benchmark_file])
            return TravelingSalesmanModel(
                points=list(points),
                depot_idx=depot_idx
            )
