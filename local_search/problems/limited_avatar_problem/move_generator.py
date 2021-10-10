from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.limited_avatar_problem.state import LimitedAvatarState
from genetic_algorithms.problems.limited_avatar_problem.moves import ChangeColor, ChangeCoordinates
from genetic_algorithms.problems.limited_avatar_problem.models.vertex import Vertex
from genetic_algorithms.problems.limited_avatar_problem.models.color import Color
from typing import Tuple, Generator, Union
import random


class LimitedAvatarMoveGenerator(MoveGenerator):
    def __init__(self, im_size: Tuple[int, int]):
        self.im_size = im_size

    def _generate_coords_diff(self) -> Tuple[int, int]:
        return (random.randint(-self.im_size[0] // 2, self.im_size[0] // 2),
                random.randint(-self.im_size[1] // 2, self.im_size[1] // 2))

    def _generate_vertex_idx(self, state: LimitedAvatarState) -> int:
        return random.randint(0, state.model.n_polygon_vertices - 1)

    def _generate_color_diff(self) -> Color:
        return Color(R=random.randint(-255, 255),
                     G=random.randint(-255, 255),
                     B=random.randint(-255, 255),
                     A=random.randint(-255, 255))

    def _generate_move(self, state: LimitedAvatarState):
        while True:
            polygon_idx = random.randint(0, state.model.n_polygons - 1)
            yield random.choice(
                [ChangeColor(state, polygon_idx, self._generate_color_diff()),
                 ChangeCoordinates(state, polygon_idx, self._generate_vertex_idx(state), self._generate_coords_diff())]
            )

    def random_moves(self, state: LimitedAvatarState) -> Generator[Union[ChangeColor, ChangeCoordinates], None, None]:
        return self._generate_move(state)

    def available_moves(self, state: LimitedAvatarState) -> Generator[Union[ChangeColor, ChangeCoordinates], None, None]:
        return self._generate_move(state)
