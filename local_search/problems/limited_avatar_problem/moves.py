from genetic_algorithms.problems.base.moves import Move
from genetic_algorithms.problems.limited_avatar_problem.state import LimitedAvatarState
from genetic_algorithms.problems.limited_avatar_problem.models.color import Color
from typing import Tuple
import copy


class ChangeColor(Move[LimitedAvatarState]):
    def __init__(self, from_state: LimitedAvatarState, polygon_idx: int, color_diff: Color):
        super().__init__(from_state)
        (self.polygon_idx, self.color_diff) = polygon_idx, color_diff

    def make(self) -> LimitedAvatarState:
        changed_polygons = copy.deepcopy(self.state.polygons)
        changed_polygons[self.polygon_idx].change_color(self.color_diff)
        return LimitedAvatarState(model=self.state.model, polygons=changed_polygons)


class ChangeCoordinates(Move[LimitedAvatarState]):
    def __init__(self, from_state: LimitedAvatarState, polygon_idx: int, vertex_idx: int, coords_diff: Tuple[int, int]):
        super().__init__(from_state)
        (self.polygon_idx, self.vertex_idx, self.coords_diff) = polygon_idx, vertex_idx, coords_diff

    def make(self) -> LimitedAvatarState:
        changed_polygons = copy.deepcopy(self.state.polygons)
        changed_polygons[self.polygon_idx].change_coords(self.vertex_idx, self.coords_diff)
        return LimitedAvatarState(model=self.state.model, polygons=changed_polygons)

