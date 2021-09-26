from genetic_algorithms.models.move_generator import MoveGenerator
from genetic_algorithms.problems.avatar_problem.state import AvatarState
from genetic_algorithms.problems.avatar_problem.moves import AddTriangle
from genetic_algorithms.problems.avatar_problem.models.vertex import Vertex
from genetic_algorithms.problems.avatar_problem.models.color import Color
from typing import Tuple, Generator
import random


class AvatarMoveGenerator(MoveGenerator):
    def __init__(self, im_size: Tuple[int, int]):
        self.im_size = im_size
        self.offset = self.im_size[0]//5

    def _generate_vertex(self) -> Vertex:
        return Vertex(x=random.randint(0-self.offset, self.im_size[0]+self.offset),
                      y=random.randint(0-self.offset, self.im_size[1]+self.offset))

    def _generate_move(self, state: AvatarState):
        while True:
            vertices = [self._generate_vertex(), self._generate_vertex(), self._generate_vertex()]
            color = self._generate_color()
            yield AddTriangle(state, vertices=vertices, color=color)

    def _generate_color(self) -> Color:
        return Color(R=random.randint(0, 0xff),
                     G=random.randint(0, 0xff),
                     B=random.randint(0, 0xff),
                     A=random.randint(0, 0xff))

    def random_moves(self, state: AvatarState) -> Generator[AddTriangle, None, None]:
        return self._generate_move(state)

    def available_moves(self, state: AvatarState) -> Generator[AddTriangle, None, None]:
        return self._generate_move(state)