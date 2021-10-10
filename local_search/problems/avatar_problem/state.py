from local_search.problems.base.state import State
from dataclasses import dataclass
from PIL import Image, ImageChops
from io import BytesIO


@dataclass
class AvatarState(State):
    image: Image.Image

    def __str__(self):
        return 'There is no string representation of avatar state.'

    def __eq__(self, other: 'AvatarState'):
        if other is None:
            return False
        return ImageChops.difference(self.image, other.image).getbbox() is None

    @staticmethod
    def to_string(image: Image.Image):
        byte_io = BytesIO()
        image.save(byte_io, 'PNG')
        return byte_io.getvalue().decode('ISO-8859-1')

    def asdict(self):
        return {
            'image': self.to_string(self.image)
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        image = Image.open(BytesIO(data['image'].encode('ISO-8859-1')))
        return cls(image)

    def show_image(self):
        self.image.show()
