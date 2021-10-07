import random
from local_search.problems.base.problem import Problem, Goal
from typing import Iterable, List, Set, Dict

from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.state import GraphColoringState

from local_search.problems.graph_coloring_problem.models.edge import Edge
from local_search.problems.graph_coloring_problem.models.vertex import Vertex
from local_search.problems.graph_coloring_problem.moves.move_generator import GraphColoringMoveGenerator


class GraphColoringProblem(Problem):

    def __init__(self, edges: List[Edge], move_generator_name: str, goal_name: str):
        self._edges: List[Edge] = edges
        self.graph: Dict[int, Set[int]] = self._create_graph()
        self.n_vertices = len(self.graph)
        move_generator = GraphColoringMoveGenerator.move_generators[move_generator_name](
            self.graph, self.n_vertices)
        goal = GraphColoringGoal.goals[goal_name](self.edges, self.n_vertices)
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution, move_generator, goal)

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

    def random_state(self) -> 'State':
        coloring = [Vertex(idx=i, color=random.randrange(self.n_vertices)) for i in range(self.n_vertices)]
        return GraphColoringState(coloring=coloring)

    @classmethod
    def from_benchmark(cls, benchmark_name: str, move_generator_name: str, goal_name: str):
        with open(cls.get_path_to_benchmarks()/benchmark_name) as benchmark_file:

            def line_to_edge(line: str):
                (start, end) = map(int, line.split(sep=' '))
                return Edge(start, end)

            edges = [line_to_edge(line) for line in benchmark_file]
            return GraphColoringProblem(edges=edges, move_generator_name=move_generator_name, goal_name=goal_name)

    @staticmethod
    def get_available_move_generation_strategies() -> Iterable[str]:
        return GraphColoringMoveGenerator.move_generators.keys()

    @staticmethod
    def get_available_goals() -> Iterable[str]:
        return GraphColoringGoal.goals.keys()