from typing import Tuple
from PIL import Image
from local_search.problems.avatar_problem.state import AvatarState
from local_search.problems.base.goal import Goal, GoalType
from local_search.problems.base.state import State


class ApproximateAvatar(Goal):

    def __init__(self, reference_image: Image.Image):
        self._ref = reference_image

    def objective_for(self, state: AvatarState) -> int:
        """
        Calculates objective for passed state
        """
        return sum(self._pix_comp(
            self._ref.getpixel((x, y)),
            state.image.getpixel((x, y))
        ) for y in range(self._ref.size[1]) for x in range(self._ref.size[0]))

    def _pix_comp(self, ref_pix: Tuple[int, int, int], pix_to_comp: Tuple[int, int, int]) -> int:
        d_r = ref_pix[0] - pix_to_comp[0]
        d_g = ref_pix[1] - pix_to_comp[1]
        d_b = ref_pix[2] - pix_to_comp[2]
        return d_r * d_r + d_g * d_g + d_b * d_b

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
