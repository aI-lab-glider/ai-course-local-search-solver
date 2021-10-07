from typing import Iterable, List
import random
from local_search.problems.base.problem import Problem, Goal
from local_search.problems.traveling_salesman_problem.models.point import \
    Point
from local_search.problems.traveling_salesman_problem.models.salesman import \
    Salesman
from local_search.problems.traveling_salesman_problem.moves.move_generator import \
    TravelingSalesmanMoveGenerator
from local_search.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState


class TravelingSalesmanProblem(Problem):

    def __init__(self, points: List[Point],
                 depot_idx: int,
                 move_generator_name: str):
        self._points: List[Point] = points
        self.depot_idx = depot_idx
        initial_solution = self.random_state()
        move_generator = TravelingSalesmanMoveGenerator.move_generators[move_generator_name](
        )
        super().__init__(initial_solution, move_generator)

    @property
    def points(self):
        return self._points

    def random_state(self) -> TravelingSalesmanState:
        route = [idx for idx in range(
            len(self._points)) if idx != self.depot_idx]
        random.shuffle(route)
        naive_circle = [self.depot_idx] + route + [self.depot_idx]
        return TravelingSalesmanState(points=self.points, route=naive_circle)

    def objective_for(self, state: TravelingSalesmanState) -> int:
        route = [self._points[i]
                 for i in state.route]
        return int(Salesman.from_point(route[0])
                           .walk_route(route)
                           .travelled_distance)

    def goal(self) -> Goal:
        return Goal.MIN

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return TravelingSalesmanMoveGenerator.move_generators.keys()

    @classmethod
    def from_benchmark(cls, benchmark_name: str, move_generator_name: str):
        with open(cls.get_path_to_benchmarks()/benchmark_name) as benchmark_file:
            depot_idx = int(benchmark_file.readline())

            def line_to_point(line: str):
                (x, y) = map(int, line.split(sep=' '))
                return Point(x, y)
            points = list(
                map(line_to_point, [line for line in benchmark_file]))
            return TravelingSalesmanProblem(
                points=list(points),
                depot_idx=depot_idx,
                move_generator_name=move_generator_name
            )
