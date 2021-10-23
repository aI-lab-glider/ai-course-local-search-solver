from typing import List

import pytest

from local_search.problems.graph_coloring_problem.goals import MinColors
from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.state import GraphColoringState
from test_utils import RelativePathLoader


@pytest.fixture()
def graph():
    return {0: {4, 5, 8}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}


@pytest.fixture()
def n_vertices(graph):
    return len(graph)


@pytest.fixture()
def edges(graph) -> List[Edge]:
    result = []
    for start, ends in graph.items():
        result += [Edge(start, end) for end in ends]
    return result


@pytest.fixture()
def teacher_goal(edges: List[Edge], n_vertices: int) -> GraphColoringGoal:
    return MinColors(edges, n_vertices)


@pytest.fixture()
def student_goal(edges: List[Edge], n_vertices: int, student_loader: RelativePathLoader) -> GraphColoringGoal:
    students_module = student_loader.load("local_search/problems/graph_coloring_problem/goals/min_colors.py")
    return students_module.MinColors(edges, n_vertices)


@pytest.fixture()
def graph_coloring_state(n_vertices: int, num_colors: int):
    colors = list(range(num_colors))
    return GraphColoringState([
        Vertex(i, colors[i % num_colors]) for i in range(n_vertices)
    ])


@pytest.mark.parametrize('num_colors', [1, 2, 4, 9])
def test_num_colors(graph_coloring_state, student_goal, teacher_goal):
    student_colors = student_goal._num_colors(graph_coloring_state)
    teacher_colors = teacher_goal._num_colors(graph_coloring_state)
    assert teacher_colors == student_colors, f'expected {teacher_colors} colors, got {student_colors}\n' \
                                             f'\t- state {graph_coloring_state},'


@pytest.mark.parametrize('num_colors', [1, 2, 4, 9])
def test_bad_edges(graph_coloring_state, student_goal, teacher_goal):
    student_bad_edges = student_goal._bad_edges(graph_coloring_state)
    teacher_bad_edges = teacher_goal._bad_edges(graph_coloring_state)
    assert teacher_bad_edges == student_bad_edges, f'expected {teacher_bad_edges} bad edges, got {student_bad_edges}\n' \
                                                   f'\t- state {graph_coloring_state},'


@pytest.mark.parametrize('num_colors', [1, 2, 4, 9])
def test_color_classes(graph_coloring_state, student_goal, teacher_goal):
    student_color_classes = student_goal._color_classes(graph_coloring_state)
    teacher_color_classes = teacher_goal._color_classes(graph_coloring_state)

    assert student_color_classes == teacher_color_classes, f'expected {teacher_color_classes} color classes, got {student_color_classes}\n' \
                                                           f'\t- state {graph_coloring_state},'
