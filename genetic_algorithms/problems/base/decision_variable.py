from dataclasses import dataclass
from typing import TypeVar

TDecisionVarValue = TypeVar("TDecisionVarValue")


@dataclass
class DecisionVariable:
    """
    Value that we are trying to optimize in problem.
    """
    idx: int  # TODO: who should be responsible for setting this index ??
    # Probably a ProblemClass, but should it be a generic method or it should a concrete one ??
    value: TDecisionVarValue
