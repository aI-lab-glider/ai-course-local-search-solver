from dataclasses import dataclass
from local_search.problems.base.problem import Problem
from typing import Generator, Iterable, List, Set, Dict, Type
from pathlib import Path

import local_search
from local_search.problems.graph_coloring_problem.state import GraphColoringState
from local_search.problems.graph_coloring_problem.moves import ChangeColor


from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.move_generator import GraphColoringMoveGenerator


class GraphColoringProblem(Problem):

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return GraphColoringMoveGenerator.move_generators.keys()

    def __init__(self, edges: List[Edge], move_generator_name: str):
        self._edges: List[Edge] = edges
        self.graph: Dict[int, Set[int]] = self._create_graph()
        self.n_vertices = len(self.graph)
        move_generator = GraphColoringMoveGenerator.move_generators[move_generator_name](
            self.n_vertices)
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution, move_generator)

    @property
    def edges(self):
        return self._edges

    def _create_graph(self) -> Dict[int, Set[int]]:
        graph = {}
        for edge in self._edges:
            if edge.start in graph.keys():
                graph[edge.start].add(edge.end)
            else:
                graph[edge.start] = {edge.end}
            if edge.end in graph.keys():
                graph[edge.end].add(edge.start)
            else:
                graph[edge.end] = {edge.start}
        return graph

    def _find_initial_solution(self) -> GraphColoringState:
        coloring = [Vertex(idx=i, color=-1) for i in range(self.n_vertices)]
        coloring[0].color = 0
        for vertex in self.graph:
            available_colors = [i for i in range(self.n_vertices)]
            for neighbour in self.graph[vertex]:
                if coloring[neighbour].color in available_colors:
                    available_colors.remove(coloring[neighbour].color)
            coloring[vertex].color = available_colors[0]
        return GraphColoringState(coloring=coloring)

    def _bad_edges(self, state: GraphColoringState) -> List[int]:
        bad_edges = [0 for _ in range(self.n_vertices)]
        for edge in self._edges:
            if state.coloring[edge.start].color == state.coloring[edge.end].color:
                bad_edges[state.coloring[edge.start].color] += 1
        return bad_edges

    def _color_classes(self, state: GraphColoringState) -> List[int]:
        color_classes = [0 for _ in range(self.n_vertices)]
        for vertex in state.coloring:
            color_classes[vertex.color] += 1
        return color_classes

    def cost_for(self, state: GraphColoringState) -> int:
        bad_edges = self._bad_edges(state)
        color_classes = self._color_classes(state)
        return sum([2*bad_edges[i]*color_classes[i]-color_classes[i]**2 for i in range(self.n_vertices)])

    @classmethod
    def from_benchmark(cls, benchmark_name: str, move_generator_name: str):
        with open(cls.get_path_to_benchmarks()/benchmark_name) as benchmark_file:

            def line_to_edge(line: str):
                (start, end) = map(int, line.split(sep=' '))
                return Edge(start, end)

            edges = [line_to_edge(line) for line in benchmark_file]
            return GraphColoringProblem(edges=edges, move_generator_name=move_generator_name)
