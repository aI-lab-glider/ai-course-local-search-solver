from genetic_algorithms.problems.base.state import State
from dataclasses import dataclass
from PIL import Image, ImageChops


@dataclass
class AvatarState(State):
    image: Image.Image

    def __str__(self):
        return str(self.image.getdata())

    def __eq__(self, other: 'AvatarState'):
        if other is None:
            return False
        return ImageChops.difference(self.image, other.image).getbbox() is None

    def show_image(self):
        self.image.show()

    def shuffle(self):
        return self
