from dataclasses import dataclass
from typing import Any, Dict, Iterable, Tuple, TypeVar

from store import NotFoundInStoreError, Schema, Store, StoreKey

A = TypeVar("A")


@dataclass
class DictStore(Store[A]):
    schema: Schema[A]
    state: Dict[str, Any] = {}
    index: int = 0

    def _next_key(self) -> str:
        self.index += 1
        key = f"{self.index}"
        return key

    async def items(self) -> Iterable[Tuple[StoreKey, A]]:
        return self.state.items()

    async def get(self, key: StoreKey) -> A:
        storable = self.state.get(key)
        return self.schema.decode(storable)

    async def add(self, value: A) -> StoreKey:
        storable = self.schema.encode(value)
        key = self._next_key()
        self.state[key] = storable
        return key

    async def update(self, key: StoreKey, value: A) -> None:
        storable = self.schema.encode(value)
        if key not in self.state:
            raise NotFoundInStoreError
        self.state[key] = storable

    async def delete(self, key: StoreKey) -> None:
        if key in self.state:
            del self.state[key]
