from local_search.problems.base.state import State
from dataclasses import dataclass
from PIL import Image, ImageChops
from io import BytesIO
import base64


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
    def to_b64(image: Image.Image):
        im_file = BytesIO()
        image.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()
        return base64.b64encode(im_bytes)

    def asdict(self):
        base = super().asdict()
        return {
            'image': f"{self.to_b64(self.image)}".replace("b'", ""),
            **base
        }

    @classmethod
    def from_dict(cls, data):
        cls.validate_data(data)
        image = Image.open(BytesIO(base64.b64decode(data['image'])))
        return cls(image)
