from abc import ABC
from typing import List

from local_search.helpers.camel_to_snake import camel_to_snake
from local_search.problems.base.problem import Goal
from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.state import GraphColoringState

# Do we want to have TODOs on this class. It not teaches students nothing about algorithms, only makes them familiar with the problem?


class GraphColoringGoal(Goal, ABC):
    """
    Base class for goals of the graph coloring problem
    """
    goals = {}

    def __init__(self, edges: List[Edge], n_vertices: int):
        self.edges = edges
        self.n_vertices = n_vertices

    def __init_subclass__(cls):
        GraphColoringGoal.goals[camel_to_snake(cls.__name__)] = cls

    def _num_colors(self, state: GraphColoringState) -> int:
        # TODO:
        # return number of colors in the coloring
        return len(set([v.color for v in state.coloring]))

    def _bad_edges(self, state: GraphColoringState) -> List[int]:
        # TODO:
        # return number of bad edges of every color class in the graph
        # tip. self.edges is the list of 'Edge' in the graph
        bad_edges = [0 for _ in range(self.n_vertices)]
        for edge in self.edges:
            if state.coloring[edge.start].color == state.coloring[edge.end].color:
                bad_edges[state.coloring[edge.start].color] += 1
        return bad_edges

    def _color_classes(self, state: GraphColoringState) -> List[int]:
        # TODO:
        # return sizes of the color classes
        color_classes = [0 for _ in range(self.n_vertices)]
        for vertex in state.coloring:
            color_classes[vertex.color] += 1
        return color_classes

    def human_readable_objective_for(self, state: GraphColoringState) -> str:
        return f"{self._num_colors(state)} colors"
