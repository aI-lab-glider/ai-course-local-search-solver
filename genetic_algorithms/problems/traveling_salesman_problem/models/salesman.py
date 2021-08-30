from math import sqrt

from genetic_algorithms.problems.traveling_salesman_problem.models.point import \
    Point


class Salesman(Point):
    walked_distance: float = 0

    def walk_to(self, point: Point) -> 'Salesman':
        self.walked_distance += sqrt((point.x - self.x)
                                     ** 2 + (self.y - point.y) ** 2)
        self.x, self.y = point.x, point.y
        return self

    @classmethod
    def from_point(cls, point: Point) -> 'Salesman':
        return cls(x=point.x, y=point.y)
