from local_search.problems.base.goal import GoalType
from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.state import GraphColoringState
import pytest
import random

N_VERTICES = 10


class MockGoal(GraphColoringGoal):
    def objective_for(self, state) -> int:
        return 1

    def human_readable_objective_for(self, state) -> str:
        return str(self.objective_for(state))

    def type(self) -> GoalType:
        return GoalType.MIN

    @staticmethod
    def from_n_vertices(n_vertices) -> 'MockGoal':
        l = list(range(n_vertices))
        edges = [Edge(start, end) for start, end in zip(l, l[1:] + [l[0]])]
        return MockGoal(edges, n_vertices)


@pytest.mark.parametrize('num_colors', [1, 2, 4, 10])
def test_num_colors(num_colors):
    colors = list(range(num_colors))
    state = GraphColoringState([
        Vertex(i, colors[i % num_colors]) for i in range(N_VERTICES)
    ])
    goal = MockGoal.from_n_vertices(N_VERTICES)
    calculated_colors = goal._num_colors(state)
    assert num_colors == calculated_colors, 'expected goal to return '\
                                            f'{num_colors} for state {state},'\
                                            f'but received {calculated_colors}'


def test_bad_edges():
    color = 1
    state = GraphColoringState([Vertex(i, color) for i in range(N_VERTICES)])
    expected_bad_edges = [0 for _ in range(N_VERTICES)]
    expected_bad_edges[color] = N_VERTICES
    goal = MockGoal.from_n_vertices(N_VERTICES)
    actual_bad_edges = goal._bad_edges(state)
    assert expected_bad_edges == actual_bad_edges, f'expected to get {expected_bad_edges} '\
                                                   f'for state {state}, but received: {actual_bad_edges}'


@pytest.mark.parametrize('num_colors', [1, 2, 4, 10])
def test_color_classes(num_colors):
    colors = list(range(num_colors))
    coloring = [Vertex(i, colors[i % num_colors])
                for i in range(N_VERTICES)]
    state = GraphColoringState(coloring)
    goal = MockGoal.from_n_vertices(N_VERTICES)

    expected_color_classes = [0 for _ in range(N_VERTICES)]
    for vertex in state.coloring:
        expected_color_classes[vertex.color] += 1

    actual_color_classes = goal._color_classes(state)

    assert actual_color_classes == expected_color_classes, f'expected actual color classes, to be {expected_color_classes}'\
                                                           f'for state {state}, but received {actual_color_classes}'
