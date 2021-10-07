
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from local_search.problems.base.state import State
from local_search.problems.traveling_salesman_problem.models.edge import \
    Edge
from random import sample


@dataclass
class TravelingSalesmanState(State):
    route: List[int]
    points: List[Tuple[int,int]]

    def __str__(self):
        return str.join(" -> ", map(lambda idx: f'({self.points[idx].x}, {self.points[idx].y})', self.route))

    @property
    def edges(self) -> Iterable[Edge]:
        not_connected_edges = zip(
            self.route,
            self.route[1:] + [self.route[0]]
        )
        return map(lambda edge: Edge(edge[0], edge[1]), not_connected_edges)

    def __eq__(self, other):
        if other is None:
            return False
        is_any_idx_differs = any(
            self.route[i] != other.route[i] for i in range(len(self.route)))
        return not is_any_idx_differs
