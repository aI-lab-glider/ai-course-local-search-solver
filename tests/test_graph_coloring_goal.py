from typing import List

import pytest

from local_search.problems.graph_coloring_problem.goals import MinColors
from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.state import GraphColoringState

GraphDict = dict[int, dict[int]]


def create_edges(graph: GraphDict) -> List[Edge]:
    result = []
    for start, ends in graph.items():
        result += [Edge(start, end) for end in ends]
    return result


@pytest.fixture()
def graph():
    return {0: {4, 5, 8}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}


def create_goal(graph: GraphDict) -> GraphColoringGoal:
    n_vertices = len(graph)
    edges = create_edges(graph)
    return MinColors(edges, n_vertices)


def create_graph_coloring_state(graph: GraphDict, num_colors: int):
    n_vertices = len(graph)
    colors = list(range(num_colors))
    return GraphColoringState([
        Vertex(i, colors[i % num_colors]) for i in range(n_vertices)
    ])


@pytest.mark.parametrize('num_colors', [5, 3, 1])
def test_num_colors(graph: GraphDict, num_colors: int):
    goal = create_goal(graph)
    state = create_graph_coloring_state(graph, num_colors)
    expected_num_colors = num_colors
    actual_num_colors = goal._num_colors(state)
    assert expected_num_colors == goal._num_colors(state), f'expected {expected_num_colors} colors, got {actual_num_colors}\n' \
        f'\t- state {state},'


@pytest.mark.parametrize('num_colors, expected', [
    (5, [2, 2, 0, 0, 0, 0, 0, 0, 0]),
    (3, [2, 2, 2, 0, 0, 0, 0, 0, 0]),
    (1, [18, 0, 0, 0, 0, 0, 0, 0, 0])
])
def test_bad_edges(graph: GraphDict, num_colors: int, expected: list[int]):
    goal = create_goal(graph)
    state = create_graph_coloring_state(graph, num_colors)
    actual_bad_edges = goal._bad_edges(state)
    assert expected == actual_bad_edges, f'expected {expected} bad edges, got {actual_bad_edges}\n' \
        f'\t- state {state},'


@pytest.mark.parametrize('num_colors, expected', [
    (5, [2, 2, 2, 2, 1, 0, 0, 0, 0]),
    (3, [3, 3, 3, 0, 0, 0, 0, 0, 0]),
    (1, [9, 0, 0, 0, 0, 0, 0, 0, 0])
])
def test_color_classes(graph: GraphDict, num_colors: int, expected: list[int]):
    goal = create_goal(graph)
    state = create_graph_coloring_state(graph, num_colors)
    actual_color_classes = goal._color_classes(state)
    assert expected == actual_color_classes, f'expected {expected} color classes, got {actual_color_classes}\n' \
        f'\t- state {state},'
