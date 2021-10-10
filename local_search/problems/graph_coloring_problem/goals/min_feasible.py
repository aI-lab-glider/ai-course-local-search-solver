from typing import List

from local_search.problems.base.goal import GoalType
from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.state import GraphColoringState


class MinFeasible(GraphColoringGoal):

    def objective_for(self, state: GraphColoringState) -> int:
        bad_edges = self._bad_edges(state)
        color_classes = self._color_classes(state)
        return sum([2*bad_edges[i]*color_classes[i]-color_classes[i]**2 for i in range(self.n_vertices)])

    def type(self) -> GoalType:
        return GoalType.MIN