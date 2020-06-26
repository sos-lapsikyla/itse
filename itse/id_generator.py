import time
from typing import Protocol, Type


class UintError(Exception):
    ...


class OutOfBoundsError(UintError):
    ...


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


class Id:
    def __init__(
        self, timestamp: Uint32, node_id: Uint16, index: Uint16,
    ) -> None:
        self.val: Uint64 = Uint64((timestamp << 32) | (node_id << 16) | index)


# TODO define get_node_id just as an async function
class NodeIdGetter(Protocol):
    async def get_node_id(self) -> Uint16:
        ...


class IdFactory:
    def __init__(self, node_id_getter: NodeIdGetter) -> None:
        self.node_id_getter = node_id_getter
        self.last_seen_time = Uint32(int(time.time()))
        self.index = 0
