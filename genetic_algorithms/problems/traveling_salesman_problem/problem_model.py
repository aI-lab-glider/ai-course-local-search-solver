from typing import Iterable, List

from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.traveling_salesman_problem.models.point import \
    Point
from genetic_algorithms.problems.traveling_salesman_problem.models.salesman import \
    Salesman
from genetic_algorithms.problems.traveling_salesman_problem.move_generator import \
    TravelingSalesmanMoveGenerator
from genetic_algorithms.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState


class TravelingSalesmanProblem(Model):

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return TravelingSalesmanMoveGenerator.move_generators.keys()

    def __init__(self, points: List[Point],
                 depot_idx: int,
                 move_generator_name: str):
        self._points: List[Point] = points
        self.depot_idx = depot_idx
        initial_solution = self._find_initial_solution()
        move_generator = TravelingSalesmanMoveGenerator.move_generators[move_generator_name](
            depot_idx)
        super().__init__(initial_solution, move_generator)

    @property
    def points(self):
        return self._points

    def _find_initial_solution(self) -> TravelingSalesmanState:
        naive_circle = list(
            range(0, len(self._points))) + [self.depot_idx]
        return TravelingSalesmanState(model=self, route=naive_circle)

    def cost_for(self, state: TravelingSalesmanState) -> int:
        route = [self._points[i]
                 for i in state.route if i != self.depot_idx]
        depot = self._points[self.depot_idx]
        return int(Salesman.from_point(depot)
                           .walk_route(route)
                           .walk_to(depot)
                           .travelled_distance)

    @classmethod
    def from_benchmark(cls, benchmark_name: str, move_generator_name: str):
        with open(cls.get_path_to_benchmarks()/benchmark_name) as benchmark_file:
            depot_idx = int(benchmark_file.readline())

            def line_to_point(line: str):
                (x, y) = map(int, line.split(sep=' '))
                return Point(x, y)
            points = map(line_to_point, [line for line in benchmark_file])
            return TravelingSalesmanProblem(
                points=list(points),
                depot_idx=depot_idx,
                move_generator_name=move_generator_name
            )
