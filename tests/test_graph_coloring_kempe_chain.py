from typing import List, Dict, Set

import pytest

from local_search.problems.graph_coloring_problem.goals import MinColors
from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.state import GraphColoringState
from test_utils import RelativePathLoader


@pytest.fixture()
def start_index():
    return 0


@pytest.fixture()
def graph() -> Dict[int, Set[int]]:
    return {0: {4,5,8}, 1: {4,6}, 2: {4,5}, 3: {6}, 4: {0, 1, 2}, 5: {0,2}, 6: {1, 3}, 7: {8}, 8: {0,7}}


@pytest.fixture()
def old_coloring_state(graph) -> GraphColoringState:
    def color(i):
        return i // 4

    return GraphColoringState([Vertex(idx, color(idx)) for idx in range(len(graph))])


@pytest.fixture()
def new_coloring_state(old_coloring_state, start_index, new_color) -> GraphColoringState:
    old_coloring_state.coloring[start_index].color = new_color
    return old_coloring_state


@pytest.fixture()
def student_move(student_loader: RelativePathLoader, graph, old_coloring_state, start_index, new_color):
    student_module = student_loader.load("local_search/problems/graph_coloring_problem/moves/kempe_chain.py")
    return student_module.KempeChainMove(graph, old_coloring_state, start_index, new_color)


@pytest.fixture()
def edges(graph: Dict[int, Set[int]]) -> List[Edge]:
    result = []
    for start, ends in graph.items():
        result += [Edge(start, end) for end in ends]
    return result


@pytest.mark.parametrize('new_color', [1,2])
def test_kempe_chain_should_have_result_with_no_conflicts(student_move, new_coloring_state, edges):
    student_move._kempe_chain(new_coloring_state.coloring)
    teacher_goal = MinColors(edges, len(student_move.graph))
    bad_edges = teacher_goal._bad_edges(new_coloring_state)
    n_bad_edges = sum(bad_edges)
    assert n_bad_edges == 0, f"there are still {n_bad_edges} conflicts after kempe chain\n" \
                                                    f"\t- bad edges: {bad_edges}\n" \
                                                    f"\t- state: {new_coloring_state}\n" \
                                                    f"\t- graph: {student_move.graph}\n"


@pytest.mark.parametrize('new_color', [1, 2])
def test_kempe_chain_should_solve_direct_conflicts(student_move, new_coloring_state):
    student_move._kempe_chain(new_coloring_state.coloring)
    for n in student_move.graph[0]:
        assert new_coloring_state.coloring[n].color != new_coloring_state.coloring[0].color, \
            f"kempe chain fails to correctly fix direct coloring conflict\n" \
                                                    f"\t- state: {new_coloring_state}\n" \
                                                    f"\t- graph: {student_move.graph}\n"


@pytest.mark.parametrize('new_color', [1])
def test_kempe_chain_should_solve_indirect_conflicts(student_move, new_coloring_state, record_property):
    record_property("points", 2)
    student_move._kempe_chain(new_coloring_state.coloring)
    assert new_coloring_state.coloring[1].color == 1 \
           and new_coloring_state.coloring[3].color == 1 \
           and new_coloring_state.coloring[6].color == 0, f"kempe chain fails to fix indirect coloring conflicts:\n" \
                                                          f"\t- state: {new_coloring_state}\n" \
                                                          f"\t- graph: {student_move.graph}\n"


@pytest.mark.parametrize('new_color', [1])
def test_kempe_chain_should_handle_cycles(student_move, new_coloring_state, record_property):
    record_property("points", 2)
    student_move._kempe_chain(new_coloring_state.coloring)
    assert new_coloring_state.coloring[2].color == 1, f"kempe chain doesn't handle correctly cycles in the graph\n" \
                                                      f"\t- state: {new_coloring_state}\n" \
                                                      f"\t- graph: {student_move.graph}\n"



