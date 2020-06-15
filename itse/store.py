from dataclasses import dataclass
from typing import (
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    NamedTuple,
    Protocol,
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


class Store(Protocol[A]):
    async def items(self) -> List[A]:
        ...

    async def get(self, identifier: str) -> Option[A]:
        ...

    async def add(self, a: A) -> str:
        ...

    async def update(self, identifier: str, a: A) -> None:
        ...


StoreFactory = Callable[[Connection, Schema[A]], Store[A]]
