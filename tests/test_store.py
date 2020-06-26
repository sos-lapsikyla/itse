from typing import Any, Optional

from pydantic import BaseModel

import pytest

from itse import DictStore
from itse.store import (
    DuplicateUniqueFieldsError,
    Schema,
    Store,
)


class Dude(BaseModel):
    name: str
    age: Optional[int]
    is_wizard: bool


dude_schema = Schema(name="dude", uniques=["name"], model=Dude)


store_implementations = [DictStore]


@pytest.fixture(params=store_implementations)
def store(request: Any) -> Store:
    return request.param(dude_schema)


harry = Dude(name="Harry", age=11, is_wizard=True)
# moomin_Troll = Dude("Moomin", 15, False)
# gandalf = Dude("Gandalf The Grey", 5000, True)


@pytest.mark.asyncio
async def test_get_set(store: Store[Dude]) -> None:
    harry_key = await store.add(harry)
    assert harry == await store.get(harry_key)


@pytest.mark.asyncio
async def test_store_is_empty_by_default(store: Store[Dude]) -> None:
    assert list(await store.items()) == []


@pytest.mark.asyncio
async def test_getting_with_bad_key_returns_none(store: Store[Dude]) -> None:
    assert await store.get("Bad key") is None


@pytest.mark.asyncio
async def test_raises_duplicate_error(store: Store[Dude]) -> None:
    first_harry = harry
    second_harry = Dude(name="Harry", age=15, is_wizard=False)
    await store.add(first_harry)
    with pytest.raises(DuplicateUniqueFieldsError) as err:
        await store.add(second_harry)
    assert err.value.fields == ["name"]
