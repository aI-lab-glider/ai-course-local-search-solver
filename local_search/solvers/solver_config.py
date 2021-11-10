from dataclasses import dataclass


@dataclass
class SolverConfig:
    time_limit: int = 60
    show_statistics: bool = False
