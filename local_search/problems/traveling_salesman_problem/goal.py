from abc import ABC
from typing import List

from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.goal import GoalType
from local_search.problems.base.problem import Goal
from local_search.problems.traveling_salesman_problem.models import Point
from local_search.problems.traveling_salesman_problem.models.salesman import \
    Salesman
from local_search.problems.traveling_salesman_problem.state import \
    TravelingSalesmanState


class TravelingSalesmanGoal(Goal, ABC):
    """
    Base class for goals of the traveling salesman problem
    """
    goals = {}

    def __init__(self, points: List[Point]):
        self._points = points

    def __init_subclass__(cls):
        TravelingSalesmanGoal.goals[camel_to_snake(cls.__name__)] = cls


class Distance(TravelingSalesmanGoal):

    def objective_for(self, state: TravelingSalesmanState) -> int:
        route = [self._points[i]
                 for i in state.route]
        return int(Salesman.from_point(route[0])
                           .walk_route(route)
                           .travelled_distance)

    def human_readable_objective_for(self, state: TravelingSalesmanState) -> str:
        return f"{self.objective_for(state)} km"

    def type(self) -> GoalType:
        return GoalType.MIN
