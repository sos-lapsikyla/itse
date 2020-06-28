import asyncio
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


class Id(Uint64):
    def __init__(
        self, timestamp: Uint32, node_id: Uint16, index: Uint16,
    ) -> None:
        self.val: Uint64 = Uint64((timestamp << 32) | (node_id << 16) | index)


# TODO define get_node_id just as an async function?
class NodeIdGetter(Protocol):
    async def get_node_id(self) -> Uint16:
        ...


class TimeGetter(Protocol):
    def get_unix_time(self) -> Uint32:
        ...


class IdFactoryEnv(Protocol, NodeIdGetter, TimeGetter):
    ...


class IdFactory:
    def __init__(self, env: IdFactoryEnv) -> None:
        self.env: IdFactory = env
        self.last_seen_time: Uint32 = env.get_unix_time()
        self.index: int = 0

    def _get_index(self, current_time: Uint32) -> int:
        if current_time == self.last_seen_time:
            self.index += 1
        else:
            self.last_seen_time = current_time
            self.index = 0
        return self.index

    async def create_id(self) -> Id:
        # NB: current_time & await, order matters here.
        node_id = await self.env.get_node_id()
        current_time = self.env.get_unix_time()
        try:
            index = Uint16(self._get_index(current_time))
            return Id(timestamp=current_time, node_id=node_id, index=index)
        except OutOfBoundsError:
            await asyncio.sleep(1)
            return await self.create_id()
