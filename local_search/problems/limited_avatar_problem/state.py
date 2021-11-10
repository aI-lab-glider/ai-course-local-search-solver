from local_search.problems.base.state import State
from local_search.problems.limited_avatar_problem.models.polygon import Polygon
from local_search.problems.limited_avatar_problem.models.vertex import Vertex
from local_search.problems.limited_avatar_problem.models.color import Color
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageChops
from typing import List, Tuple
import numpy as np


@dataclass
class LimitedAvatarState(State):
    polygons: List[Polygon]
    image_size: Tuple[int, int]

    def __str__(self):
        return 'There is no string representation of limited avatar state.'

    def __eq__(self, other: 'LimitedAvatarState'):
        if other is None:
            return False
        return np.array_equal(self.image, other.image)

    def _to_coordinates(self, vertices: List[Vertex]) -> List[Tuple[int, int]]:
        return [(vertex.x, vertex.y) for vertex in vertices]

    def _to_color_coordinates(self, color: Color) -> Tuple[int, int, int, int]:
        return color.R, color.G, color.B, color.A

    def _draw_polygon(self, polygon: Polygon, image_draw: ImageDraw):
        image_draw.polygon(self._to_coordinates(polygon.vertices),
                           fill=self._to_color_coordinates(polygon.color))

    @property
    def image(self) -> Image.Image:
        image = Image.new("RGB", self.image_size, "white")
        image_draw = ImageDraw.Draw(image, "RGBA")
        for polygon in self.polygons:
            self._draw_polygon(polygon, image_draw)
        return image

    def asdict(self):
        base = super().asdict()
        return {
            'polygons': [[[(vertex.x, vertex.y) for vertex in polygon.vertices],
                          (polygon.color.R, polygon.color.G, polygon.color.B, polygon.color.A)]
                         for polygon in self.polygons],
            'image_size': self.image_size,
            **base
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        data['polygons'] = [Polygon(vertices=[Vertex(x=vertex[0], y=vertex[1]) for vertex in polygon[0]],
                                    color=Color(polygon[1][0], polygon[1][1], polygon[1][2], polygon[1][3]))
                            for polygon in data['polygons']]
        return cls(**data)
