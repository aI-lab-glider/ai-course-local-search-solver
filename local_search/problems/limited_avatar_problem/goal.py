from typing import Tuple
from PIL import Image
from local_search.problems.limited_avatar_problem.state import LimitedAvatarState
from local_search.problems.base.goal import Goal, GoalType
import numpy as np


class ApproximateLimitedAvatar(Goal):

    def __init__(self, reference_image: Image.Image):
        self._ref = np.asarray(reference_image, dtype=int)

    def objective_for(self, state: LimitedAvatarState) -> int:
        """
        Calculates objective for passed state
        """
        return ((self._ref - np.asarray(state.image)) ** 2).sum()

    def human_readable_objective_for(self, state: LimitedAvatarState) -> str:
        """
        Shows human readable objective
        """
        return f'Pixel wise difference: {self.objective_for(state)}'

    def type(self) -> GoalType:
        """
        Returns the problem goal, i.e. whether we minimize or rather maximize the objective
        """
        return GoalType.MIN
