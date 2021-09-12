from functools import reduce
from math import sqrt
from typing import List

from genetic_algorithms.problems.traveling_salesman_problem.models.point import Point


class Salesman(Point):
    travelled_distance: float = 0

    def walk_to(self, point: Point) -> "Salesman":
        self.walked_distance += sqrt((point.x - self.x)
                                     ** 2 + (self.y - point.y) ** 2)
        self.x, self.y = point.x, point.y
        return self

    def walk_route(self, route: List[Point]) -> 'Salesman':
        return reduce(lambda salesman, new_point: salesman.walk_to(new_point),
                      route,
                      self)

    @classmethod
    def from_point(cls, point: Point) -> "Salesman":
        return cls(x=point.x, y=point.y)
