
from typing import Type
from inspect import getmro, signature


def get_type_for_param(callable: Type, param_name: str):
    mro = getmro(callable)
    for method in mro:
        params = signature(method).parameters
        if param_name in params:
            return params[param_name].annotation
    return None
