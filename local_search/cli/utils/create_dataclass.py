from dataclasses import fields
from typing import Type
from enum import Enum
from local_search.cli.utils.prompt import get_or_prompt_if_not_exists_or_invalid


def create_dataclass(options, dataclass: Type):
    dataclass_config = {}

    for field in fields(dataclass):
        if issubclass(field.type, Enum):
            value = get_or_prompt_if_not_exists_or_invalid(options, field.name, {
                'default': field.default.value
            })
            field_value = field.type(value)
        else:
            field_value = get_or_prompt_if_not_exists_or_invalid(options, field.name, {
                'default': field.default,
                'type': field.type
            })

        dataclass_config[field.name] = field_value
    return dataclass(**dataclass_config)
