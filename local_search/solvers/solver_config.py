from dataclasses import dataclass


@dataclass
class SolverConfig:
    max_iter: int = 1000
    time_limit: int = 60
    show_statistics: bool = False
