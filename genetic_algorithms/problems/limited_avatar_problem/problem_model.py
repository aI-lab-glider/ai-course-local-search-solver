from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.limited_avatar_problem.move_generator import LimitedAvatarMoveGenerator
from genetic_algorithms.problems.limited_avatar_problem.state import LimitedAvatarState
from genetic_algorithms.problems.limited_avatar_problem.models.color import Color
from genetic_algorithms.problems.limited_avatar_problem.models.vertex import Vertex
from genetic_algorithms.problems.limited_avatar_problem.models.polygon import Polygon
import genetic_algorithms
from typing import Tuple
from pathlib import Path
import random
from PIL import Image


class LimitedAvatarModel(Model):
    def __init__(self, reference_image: Image):
        self.n_polygons = 50
        self.n_polygon_vertices = 3
        self.reference_image = reference_image
        self.image_size = reference_image.size
        move_generator = LimitedAvatarMoveGenerator(self.image_size)
        initial_solution = self._find_initial_solution()
        super().__init__(initial_solution, move_generator)

    def _find_initial_solution(self) -> LimitedAvatarState:
        def _generate_color() -> Color:
            return Color(R=random.randint(0, 255),
                         G=random.randint(0, 255),
                         B=random.randint(0, 255),
                         A=random.randint(0, 255))

        def _generate_vertex() -> Vertex:
            offset = self.image_size[0]//5
            return Vertex(x=random.randint(0 - offset, self.image_size[0] + offset),
                          y=random.randint(0 - offset, self.image_size[1] + offset))

        polygons = [Polygon(vertices=[_generate_vertex() for _ in range(self.n_polygon_vertices)],
                            color=_generate_color()) for _ in range(self.n_polygons)]
        return LimitedAvatarState(model=self, polygons=polygons)

    def _pix_comp(self, ref_pix: Tuple[int, int, int], pix_to_comp: Tuple[int, int, int]) -> int:
        d_r = ref_pix[0] - pix_to_comp[0]
        d_g = ref_pix[1] - pix_to_comp[1]
        d_b = ref_pix[2] - pix_to_comp[2]
        return d_r * d_r + d_g * d_g + d_b * d_b

    def cost_for(self, state: LimitedAvatarState) -> int:
        return sum(self._pix_comp(self.reference_image.getpixel((x, y)), state.image.getpixel((x, y)))
                   for y in range(self.image_size[1]) for x in range(self.image_size[0]))

    @staticmethod
    def from_benchmark(benchmark_name: str):
        img = Image.open(Path(
                genetic_algorithms.__file__).parent / "problems" / "avatar_problem" / "benchmarks" / benchmark_name)
        return LimitedAvatarModel(img)
