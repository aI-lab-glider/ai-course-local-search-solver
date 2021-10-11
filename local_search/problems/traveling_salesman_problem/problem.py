from io import TextIOWrapper
from typing import Iterable, List, Union
import random
from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.problem import Problem, Goal
from local_search.problems.traveling_salesman_problem.goal import TravelingSalesmanGoal, Distance
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
                 move_generator_name: Union[str, None] = None,
                 goal_name: Union[str, None] = "distance"):
        self._points: List[Point] = points
        self.depot_idx = depot_idx
        initial_solution = self.random_state()
        move_generator_name = move_generator_name or list(
            self.get_available_move_generation_strategies())[0]
        move_generator = TravelingSalesmanMoveGenerator.move_generators[move_generator_name](
        )
        goal_name = goal_name or list(self.get_available_goals())[0]
        goal = TravelingSalesmanGoal.goals[goal_name](self._points)
        super().__init__(initial_solution, move_generator, goal)

    @property
    def points(self):
        return self._points

    def random_state(self) -> TravelingSalesmanState:
        route = [idx for idx in range(
            len(self._points)) if idx != self.depot_idx]
        random.shuffle(route)
        naive_circle = [self.depot_idx] + route + [self.depot_idx]
        return TravelingSalesmanState(points=self.points, route=naive_circle)

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return TravelingSalesmanMoveGenerator.move_generators.keys()

    @staticmethod
    def get_available_goals() -> Iterable[str]:
        return TravelingSalesmanGoal.goals.keys()

    @classmethod
    def from_benchmark(cls, benchmark_name: str, move_generator_name: str = None, goal_name: str = "distance"):
        with open(cls.get_path_to_benchmarks()/benchmark_name) as benchmark_file:
            depot_idx, points = cls.parse_model(benchmark_file)
            return cls(
                points=points,
                depot_idx=depot_idx,
                move_generator_name=move_generator_name,
                goal_name=goal_name
            )

    @classmethod
    def parse_model(cls, file_buffer: TextIOWrapper):
        depot_idx = int(file_buffer.readline())

        def line_to_point(line: str):
            (x, y) = map(int, line.split(sep=' '))
            return Point(x, y)
        points = list(
            map(line_to_point, [line for line in file_buffer]))
        return depot_idx, points

    @classmethod
    def parse_route(cls, file_buffer: TextIOWrapper):
        idxs = file_buffer.readline().replace('State:', '').strip().split(' ')
        return list(map(int, idxs))

    def asdict(self):
        base = super().asdict()
        return {
            'depot_idx': self.depot_idx,
            'points': [(point.x, point.y) for point in self.points],
            **base
        }

    @classmethod
    def from_dict(cls, data):
        data['points'] = [Point(x=point_tuple[0], y=point_tuple[1])
                          for point_tuple in data['points']]
        return cls(**data)
