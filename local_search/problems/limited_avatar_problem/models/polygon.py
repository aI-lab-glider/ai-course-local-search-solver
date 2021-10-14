from dataclasses import dataclass
from typing import List, Tuple
from local_search.problems.limited_avatar_problem.models.vertex import Vertex
from local_search.problems.limited_avatar_problem.models.color import Color


@dataclass
class Polygon:
    vertices: List[Vertex]
    color: Color

    def change_color(self, color_diff: Color):
        self.color.R = (self.color.R + color_diff.R) % 256
        self.color.G = (self.color.G + color_diff.G) % 256
        self.color.B = (self.color.B + color_diff.B) % 256
        self.color.A = (self.color.A + color_diff.A) % 256

    def change_coords(self, vertex_idx: int, coords_diff: Tuple[int, int]):
        self.vertices[vertex_idx].x += coords_diff[0]
        self.vertices[vertex_idx].y += coords_diff[1]
