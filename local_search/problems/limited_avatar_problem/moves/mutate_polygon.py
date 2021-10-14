from local_search.problems.limited_avatar_problem.moves.move_generator import LimitedAvatarMoveGenerator
from local_search.problems.base.moves import Move
from local_search.problems.limited_avatar_problem.state import LimitedAvatarState
from local_search.problems.limited_avatar_problem.models.color import Color
from typing import Generator, Tuple, Union
import random
import copy


class MutatePolygon(LimitedAvatarMoveGenerator):
    def _generate_coords_diff(self) -> Tuple[int, int]:
        return (random.randint(-self.im_size[0] // 2, self.im_size[0] // 2),
                random.randint(-self.im_size[1] // 2, self.im_size[1] // 2))

    def _generate_vertex_idx(self, state: LimitedAvatarState) -> int:
        return random.randint(0, len(state.polygons[0].vertices) - 1)

    def _generate_color_diff(self) -> Color:
        return Color(R=random.randint(-255, 255),
                     G=random.randint(-255, 255),
                     B=random.randint(-255, 255),
                     A=random.randint(-255, 255))

    def _generate_move(self, state: LimitedAvatarState):
        while True:
            polygon_idx = random.randint(0, len(state.polygons) - 1)
            yield random.choice(
                [ChangeColorMove(state, polygon_idx, self._generate_color_diff()),
                 ChangeCoordinatesMove(state, polygon_idx, self._generate_vertex_idx(state), self._generate_coords_diff())]
            )

    def random_moves(self, state: LimitedAvatarState)-> Generator[Union['ChangeColorMove', 'ChangeCoordinatesMove'], None, None]:
        return self._generate_move(state)

    def available_moves(self, state: LimitedAvatarState) -> Generator[Union['ChangeColorMove', 'ChangeCoordinatesMove'], None, None]:
        return self._generate_move(state)


class ChangeCoordinatesMove(Move[LimitedAvatarState]):
    def __init__(self, from_state: LimitedAvatarState, polygon_idx: int, vertex_idx: int, coords_diff: Tuple[int, int]):
        super().__init__(from_state)
        (self.polygon_idx, self.vertex_idx, self.coords_diff) = polygon_idx, vertex_idx, coords_diff

    def make(self) -> LimitedAvatarState:
        changed_polygons = copy.deepcopy(self.state.polygons)
        changed_polygons[self.polygon_idx].change_coords(self.vertex_idx, self.coords_diff)
        return LimitedAvatarState(polygons=changed_polygons, image_size=self.state.image_size)


class ChangeColorMove(Move[LimitedAvatarState]):
    def __init__(self, from_state: LimitedAvatarState, polygon_idx: int, color_diff: Color):
        super().__init__(from_state)
        (self.polygon_idx, self.color_diff) = polygon_idx, color_diff

    def make(self) -> LimitedAvatarState:
        changed_polygons = copy.deepcopy(self.state.polygons)
        changed_polygons[self.polygon_idx].change_color(self.color_diff)
        return LimitedAvatarState(polygons=changed_polygons, image_size=self.state.image_size)