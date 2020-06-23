from dataclasses import dataclass
from typing import (
    Callable,
    Dict,
    Generic,
    Iterable,
    NamedTuple,
    NewType,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
)


class Connection(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...


A = TypeVar("A")


Storable = Dict[str, Union[str, int, bool]]


class Schema(Protocol[A]):
    name: str
    unique_fields: List[str]

    def decode(storable: Storable) -> A:
        ...

    def encode(a: A) -> Storable:
        ...


StoreKey = NewType("StoreKey", str)


class Store(Protocol[A]):
    async def items(self) -> Iterable[Tuple[StoreKey, A]]:
        ...

    async def get(self, key: StoreKey) -> Optional[A]:
        ...

    async def add(self, a: A) -> StoreKey:
        ...

    async def update(self, key: StoreKey, a: A) -> None:
        ...

    async def delete(self, key: StoreKey) -> None:
        ...


class StoreError(Exception):
    """Base class for exceptions in this modulule"""

    ...


@dataclass
class NotFoundInStoreError(StoreError):
    key: StoreKey


@dataclass
class DecodeError(StoreError):
    reason: str


StoreFactory = Callable[[Connection, Schema[A]], Store[A]]
