from genetic_algorithms.problems.base.state import State
from dataclasses import dataclass
from PIL import Image


@dataclass
class AvatarState(State):
    image: Image

    def __str__(self):
        return self.image.getdata()

    def show_image(self):
        self.image.show()