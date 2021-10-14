from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Union
from enum import Enum


@dataclass
class AlgorithmConfig:
    local_optimum_moves_threshold: int = 10
    local_optimum_escapes_max: int = -1  # -1 means "infinity"

    def asdict(self):
        return asdict(self)


DEFAULT_CONFIG = AlgorithmConfig()
