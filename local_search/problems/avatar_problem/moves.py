from local_search.problems.base.moves import Move
from local_search.problems.avatar_problem.state import AvatarState
from local_search.problems.avatar_problem.models.vertex import Vertex
from local_search.problems.avatar_problem.models.color import Color
from typing import List, Tuple
from PIL import ImageDraw


class AddTriangle(Move[AvatarState]):
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
