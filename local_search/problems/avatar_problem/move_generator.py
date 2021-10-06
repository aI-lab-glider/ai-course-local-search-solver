from local_search.problems.base.move_generator import MoveGenerator
from local_search.problems.avatar_problem.state import AvatarState
from local_search.problems.avatar_problem.moves import AddTriangle
from local_search.problems.avatar_problem.models.vertex import Vertex
from local_search.problems.avatar_problem.models.color import Color
from typing import Tuple, Generator
from random import randint


class AvatarMoveGenerator(MoveGenerator):
    def __init__(self, im_size: Tuple[int, int]):
        self.im_size = im_size
        self.offset = self.im_size[0]//5

    def _generate_vertex(self) -> Vertex:
        return Vertex(x=randint(0-self.offset, self.im_size[0]+self.offset),
                      y=randint(0-self.offset, self.im_size[1]+self.offset))

    def _generate_move(self, state: AvatarState):
        while True:
            vertices = [self._generate_vertex() for _ in range(3)]
            color = self._generate_color()
            yield AddTriangle(state, vertices=vertices, color=color)

    def _generate_color(self) -> Color:
        return Color(R=randint(0, 255),
                     G=randint(0, 255),
                     B=randint(0, 255),
                     A=randint(0, 255))

    def random_moves(self, state: AvatarState) -> Generator[AddTriangle, None, None]:
        return self._generate_move(state)

    def available_moves(self, state: AvatarState) -> Generator[AddTriangle, None, None]:
        return self._generate_move(state)
