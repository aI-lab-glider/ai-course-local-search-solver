from dataclasses import dataclass


@dataclass
class Vertex:
    idx: int
    color: int

    def __hash__(self):
        return hash((self.idx, self.color))

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.idx == other.color and self.color == other.color
        return False
