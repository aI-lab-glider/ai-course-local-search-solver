from typing import Tuple
from PIL import Image
from local_search.problems.avatar_problem.state import AvatarState
from local_search.problems.base.goal import Goal, GoalType
from local_search.problems.base.state import State
import numpy as np


class ApproximateAvatar(Goal):

    def __init__(self, reference_image: Image.Image):
        self._ref = np.asarray(reference_image, dtype=int)

    def objective_for(self, state: AvatarState) -> int:
        """
        Calculates objective for passed state
        """
        return ((np.asarray(state.image, dtype=int) - self._ref) ** 2).sum()

    def human_readable_objective_for(self, state: AvatarState) -> str:
        """
        Shows human readable objective
        """
        return f'Pixel wise difference: {self.objective_for(state)}'

    def type(self) -> GoalType:
        """
        Returns the problem goal, i.e. whether we minimize or rather maximize the objective
        """
        return GoalType.MIN
