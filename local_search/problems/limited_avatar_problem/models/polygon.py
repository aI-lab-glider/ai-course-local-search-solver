from dataclasses import dataclass
from typing import List, Tuple
from local_search.problems.limited_avatar_problem.models.vertex import Vertex
from local_search.problems.limited_avatar_problem.models.color import Color
import numpy as np


@dataclass
class Polygon:
    vertices: List[Vertex]
    color: Color

    def change_color(self, color_diff: Color):
        self.color.R = int(np.clip(self.color.R + color_diff.R, a_min=0, a_max=255))
        self.color.G = int(np.clip(self.color.G + color_diff.G, a_min=0, a_max=255))
        self.color.B = int(np.clip(self.color.B + color_diff.B, a_min=0, a_max=255))
        self.color.A = int(np.clip(self.color.A + color_diff.A, a_min=0, a_max=255))

    def change_coords(self, vertex_idx: int, coords_diff: Tuple[int, int]):
        self.vertices[vertex_idx].x += coords_diff[0]
        self.vertices[vertex_idx].y += coords_diff[1]
