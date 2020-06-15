from dataclasses import dataclass
from typing import (
    Callable,
    Dict,
    Generic,
    Iterable,
    Literal,
    NamedTuple,
    NewType,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)


class Connection(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...


Kind = Literal["StrKind", "IntKind", "BoolKind"]


class Field(NamedTuple):
    kind: Kind
    required: bool
    unique: bool


A = TypeVar("A")


Storable = Dict[str, Union[str, int, bool]]


@dataclass
class Schema(Generic[A]):
    name: str
    fields: Dict[str, Field]
    decode: Callable[[Storable], A]
    encode: Callable[[A], Storable]


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
