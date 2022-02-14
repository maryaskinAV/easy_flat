import typing
from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls) -> typing.Tuple[str, str]:
        return ((x.name, x.value) for x in cls)
