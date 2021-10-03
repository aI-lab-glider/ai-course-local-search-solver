from dataclasses import astuple, dataclass


@dataclass
class Edge:
    start: int
    end: int

    def __eq__(self, other):
        #TODO to remove
        return len(set(astuple(self)) - set(astuple(other))) == 0