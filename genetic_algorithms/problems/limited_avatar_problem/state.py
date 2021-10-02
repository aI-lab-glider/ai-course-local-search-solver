from genetic_algorithms.problems.base.state import State
from genetic_algorithms.problems.limited_avatar_problem.models.polygon import Polygon
from genetic_algorithms.problems.limited_avatar_problem.models.vertex import Vertex
from genetic_algorithms.problems.limited_avatar_problem.models.color import Color
from dataclasses import dataclass
from PIL import Image, ImageDraw
from typing import List, Tuple


@dataclass
class LimitedAvatarState(State):
    polygons: List[Polygon]

    def __str__(self):
        return self.image.getdata()

    def _to_coordinates(self, vertices: List[Vertex]) -> List[Tuple[int, int]]:
        return [(vertex.x, vertex.y) for vertex in vertices]

    def _to_color_coordinates(self, color: Color) -> Tuple[int, int, int, int]:
        return color.R, color.G, color.B, color.A

    def _draw_polygon(self, polygon: Polygon, image_draw: ImageDraw):
        image_draw.polygon(self._to_coordinates(polygon.vertices),
                           fill=self._to_color_coordinates(polygon.color))

    @property
    def image(self) -> Image:
        image = Image.new("RGB", self.model.image_size, "white")
        image_draw = ImageDraw.Draw(image, "RGBA")
        for polygon in self.polygons:
            self._draw_polygon(polygon, image_draw)
        return image

    def show_image(self):
        self.image.show()

