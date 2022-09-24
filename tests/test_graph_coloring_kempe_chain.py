from typing import List, Dict, Set

import pytest

from local_search.problems.graph_coloring_problem.goals import MinColors
from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.moves.kempe_chain import KempeChainMove
from local_search.problems.graph_coloring_problem.state import GraphColoringState


@pytest.fixture()
def start_index():
    return 0


@pytest.fixture()
def graph() -> dict[int, Set[int]]:
    return {0: {4, 5, 8}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}


@pytest.fixture()
def old_state(graph) -> GraphColoringState:
    def color(i):
        return i // 4
    return GraphColoringState([Vertex(idx, color(idx)) for idx in range(len(graph))])


@pytest.fixture()
def new_state(old_state, start_index, new_color) -> GraphColoringState:
    old_state.coloring[start_index].color = new_color
    return old_state


@pytest.fixture()
def student_move(graph, old_state, start_index, new_color):
    return KempeChainMove(graph, old_state, start_index, new_color)


@pytest.fixture()
def edges(graph: Dict[int, Set[int]]) -> List[Edge]:
    result = []
    for start, ends in graph.items():
        result += [Edge(start, end) for end in ends]
    return result


@pytest.mark.parametrize('new_color', [3, 5])
def test_kempe_chain_should_have_result_with_no_conflicts(student_move, new_state, edges):
    student_move._kempe_chain(new_state.coloring)
    goal = MinColors(edges, len(student_move.graph))
    bad_edges = goal._bad_edges(new_state)
    n_bad_edges = sum(bad_edges)
    assert n_bad_edges == 0, f"there are still {n_bad_edges} conflicts after kempe chain\n" \
                             f"\t- bad edges: {bad_edges}\n" \
                             f"\t- state: {new_state}\n" \
                             f"\t- graph: {student_move.graph}\n"


@pytest.mark.parametrize('new_color', [3, 5])
def test_kempe_chain_should_solve_direct_conflicts(student_move, new_state):
    student_move._kempe_chain(new_state.coloring)
    for n in student_move.graph[0]:
        assert new_state.coloring[n].color != new_state.coloring[0].color, \
            f"kempe chain fails to correctly fix direct coloring conflict\n" \
            f"\t- state: {new_state}\n" \
            f"\t- graph: {student_move.graph}\n"


@pytest.mark.parametrize('new_color', [2])
def test_kempe_chain_should_solve_indirect_conflicts(student_move, new_state):
    student_move._kempe_chain(new_state.coloring)
    assert new_state.coloring[1].color == 0 \
        and new_state.coloring[3].color == 0 \
        and new_state.coloring[6].color == 1, f"kempe chain fails to fix indirect coloring conflicts:\n" \
        f"\t- state: {new_state}\n" \
        f"\t- graph: {student_move.graph}\n"


@pytest.mark.parametrize('new_color', [2])
def test_kempe_chain_should_handle_cycles(student_move, new_state):
    student_move._kempe_chain(new_state.coloring)
    assert new_state.coloring[2].color == 0, f"kempe chain doesn't handle correctly cycles in the graph\n" \
        f"\t- state: {new_state}\n" \
        f"\t- graph: {student_move.graph}\n"
