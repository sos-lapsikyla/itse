from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
)

from pydantic import BaseModel


class Connection(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...


BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


@dataclass(frozen=True)
class Schema(Generic[BaseModelType]):
    name: str
    uniques: List[str]
    model: Type[BaseModelType]


A = TypeVar("A")


class Store(Protocol[A]):
    async def items(self) -> Iterable[Tuple[str, A]]:
        ...

    async def get(self, key: str) -> Optional[A]:
        ...

    async def add(self, a: A) -> str:
        ...

    async def update(self, key: str, a: A) -> None:
        ...

    async def delete(self, key: str) -> None:
        ...


class StoreError(Exception):
    """Base class for exceptions in this modulule"""

    ...


@dataclass()
class DuplicateUniqueFieldsError(StoreError):
    fields: List[str]


StoreFactory = Callable[[Connection, Schema], Store[A]]
