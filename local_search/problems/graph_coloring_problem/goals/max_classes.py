from local_search.problems.base.goal import GoalType
from local_search.problems.graph_coloring_problem.goals.goal import GraphColoringGoal
from local_search.problems.graph_coloring_problem.state import GraphColoringState


class MaxClasses(GraphColoringGoal):

    def objective_for(self, state: GraphColoringState) -> int:
        color_classes = self._color_classes(state)
        return sum([cc ** 2 for cc in color_classes])

    def type(self) -> GoalType:
        return GoalType.MAX