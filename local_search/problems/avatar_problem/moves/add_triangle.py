from random import randint
from local_search.problems.avatar_problem.moves.move_generator import AvatarMoveGenerator
from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.base.moves import Move
from local_search.problems.avatar_problem.state import AvatarState
from local_search.problems.avatar_problem.models.vertex import Vertex
from local_search.problems.avatar_problem.models.color import Color
from typing import Generator, List, Tuple
from PIL import ImageDraw


class AddTriangle(AvatarMoveGenerator):
    def _generate_vertex(self) -> Vertex:
        return Vertex(x=randint(0-self.offset, self.im_size[0]+self.offset),
                      y=randint(0-self.offset, self.im_size[1]+self.offset))

    def _generate_move(self, state: AvatarState):
        while True:
            vertices = [self._generate_vertex() for _ in range(3)]
            color = self._generate_color()
            yield AddTriangleMove(state, vertices=vertices, color=color)

    def _generate_color(self) -> Color:
        return Color(R=randint(0, 255),
                     G=randint(0, 255),
                     B=randint(0, 255),
                     A=randint(0, 255))

    def random_moves(self, state: AvatarState) -> Generator['AddTriangleMove', None, None]:
        return self._generate_move(state)

    def available_moves(self, state: AvatarState) -> Generator['AddTriangleMove', None, None]:
        return self._generate_move(state)


class AddTriangleMove(Move[AvatarState]):
    def __init__(self, from_state: AvatarState, vertices: List[Vertex], color: Color):
        super().__init__(from_state)
        (self.coordinates, self.color) = self._to_coordinates(
            vertices), self._to_color_coordinates(color)

    def _to_coordinates(self, vertices: List[Vertex]) -> List[Tuple[int, int]]:
        return [(vertex.x, vertex.y) for vertex in vertices]

    def _to_color_coordinates(self, color: Color) -> Tuple[int, int, int, int]:
        return color.R, color.G, color.B, color.A

    def make(self) -> AvatarState:
        new_image = self.state.image.copy()
        new_image_draw = ImageDraw.Draw(new_image, "RGBA")
        new_image_draw.polygon(
            self.coordinates, fill=self.color, outline=self.color)
        return AvatarState(image=new_image)
