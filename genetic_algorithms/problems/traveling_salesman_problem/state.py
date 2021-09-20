
from dataclasses import dataclass
from typing import Iterable, List

from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.traveling_salesman_problem.models.edge import \
    Edge


@dataclass
class TravelingSalesmanState(State):
    route: List[int]

    def __str__(self):
        return str.join(" -> ", map(lambda idx: f'({self.model.points[idx].x}, {self.model.points[idx].y})', self.route))

    @property
    def edges(self) -> Iterable[Edge]:
        not_connected_edges = zip(
            self.route,
            self.route[1:] + [self.route[0]]
        )
        return map(lambda edge: Edge(edge[0], edge[1]), not_connected_edges)
