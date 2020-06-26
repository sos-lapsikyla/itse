from typing import Any, Dict, Iterable, Optional, Set, Tuple, TypeVar

from pydantic import BaseModel

from .store import (
    DuplicateUniqueFieldsError,
    Schema,
    Store,
)


A = TypeVar("A", bound=BaseModel)


class DictStore(Store[A]):
    def __init__(self, schema: Schema) -> None:
        self.model = schema.model
        self.uniques: Dict[str, Set[Any]] = {
            field: set() for field in schema.uniques
        }
        self.state: Dict[str, Any] = {}
        self.index: int = 0

    def _next_key(self) -> str:
        self.index += 1
        key = f"{self.index}"
        return key

    async def items(self) -> Iterable[Tuple[str, A]]:
        return self.state.items()

    async def get(self, key: str) -> Optional[A]:
        if not (storable := self.state.get(key)):
            return None
        return self.model(**storable)

    async def add(self, item: A) -> str:
        storable = item.dict()

        requested_uniques = {}
        for field_name in self.uniques:
            if (value := storable[field_name]) is not None:
                requested_uniques[field_name] = value

        failed_uniques = [
            field_name
            for field_name, value in requested_uniques.items()
            if value in self.uniques[field_name]
        ]
        if failed_uniques:
            raise DuplicateUniqueFieldsError(fields=failed_uniques)

        for field_name, value in requested_uniques.items():
            self.uniques[field_name].add(value)

        key = self._next_key()
        self.state[key] = storable
        return key

    async def update(self, key: str, item: A) -> None:
        storable = item.dict()
        if key not in self.state:
            raise NotFoundInStoreError
        self.state[key] = storable

    async def delete(self, key: str) -> None:
        if key in self.state:
            del self.state[key]
