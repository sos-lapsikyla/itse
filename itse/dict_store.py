from dataclasses import dataclass
from typing import Any, Dict

from store import Schema, Store

A = TypeVar("A")

@dataclass
class DictStore(Store[A])
    schema: Schema[A]
    state: Dict[str, Any] = {}
    next_id: int = 0

    async def get(self, identifier: str) -> A:
        elem = self.state[identifier]
        schema.decode

