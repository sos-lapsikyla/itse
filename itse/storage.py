from typing import List, Protocol, TypeVar


class Connection(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...


A = TypeVar("A")


class Storage(Protocol[A]):
    async def read_all(self) -> List[A]:
        ...

    async def read_one(self, identifier: str) -> A:
        ...

    async def create(self, a: A) -> str:
        """Returns identifier str."""
        ...

    async def update(self, identifier: str, a: A) -> None:
        ...

    async def delete(self, identifier: str) -> None:
        ...


#    def unique
#    def constant
#    def finalize


# unique(constant(base_type))
# constant(unique(base_type))
# base_type.less_than.more_than.eq

# Schema = Mapping[str, Val]
