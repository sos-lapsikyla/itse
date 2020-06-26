import time
from typing import Any, List, NamedTuple, Type, TypeVar


class UintError(Exception):
    ...


class OutOfBoundsError(UintError):
    ...


# TODO fix repetition
# Dunno how to handle dynamic class creation with mypy


class Uint64(int):
    def __new__(cls: Type["Uint64"], val: int) -> "Uint64":
        if val < 0 or val >= 2 ** 64:
            raise OutOfBoundsError()
        return super(cls, Uint64).__new__(cls, val)


class Uint32(int):
    def __new__(cls: Type["Uint32"], val: int) -> "Uint32":
        if val < 0 or val >= 2 ** 32:
            raise OutOfBoundsError()
        return super(cls, Uint32).__new__(cls, val)


class Uint16(int):
    def __new__(cls: Type["Uint16"], val: int) -> "Uint16":
        if val < 0 or val >= 2 ** 16:
            raise OutOfBoundsError()
        return super(cls, Uint16).__new__(cls, val)


def Uint64Id(Uint64):
    def __new__(
        cls: Type["Id"], timestamp: Uint32, node_id: Uint16, index: Uint16
    ) -> Id:
        val = (timestamp << 32) | (node_id << 16) | index
        return super(cls, Uint64).__new__(cls, val)



class NodeIdGiver(Protocol):
    async def gimmeNodeId(self) -> Uint16:
        ...


class IdFactory:
    def __init__(self, idGiverNodeIdGiver) -> None:

