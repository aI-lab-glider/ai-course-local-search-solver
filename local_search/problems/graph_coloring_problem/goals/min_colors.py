from local_search.problems.base.goal import GoalType
from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.state import GraphColoringState


class MinColors(GraphColoringGoal):

    def objective_for(self, state: GraphColoringState) -> int:
        return self._num_colors(state)

    def type(self) -> GoalType:
        return GoalType.MIN