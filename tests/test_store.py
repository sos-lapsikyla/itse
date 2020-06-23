from operator import itemgetter
from typing import Any, NamedTuple, Optional

import pytest

from itse.dict_store import DictStore
from itse.store import Schema


class Dude(NamedTuple):
    name: str
    age: Optional[int]
    is_wizard: bool


class DudeSchema(Schema):
    name: "Dude"
    unique_fields = ["name"]
    def decode(storable: Storable) -> Dude:


dude_fields = {
    "name": Field(kind="str", required=True, unique=True),
    "age": Field(kind="int", required=False, unique=False),
    "is_wizard": Field(kind="bool", required=True, unique=False),
}


def encode_dude(dude: Dude) -> store.Storable:
    name, age, is_wizard = dude
    return {
        "name": name,
        "age": age,
        "is_wizard": is_wizard,
    }


def decode_dude(storable: store.Storable) -> Dude:
    slots = {"name": str, "age": int, "is_wizard": bool}
    for field_name, expected_type in slots:
        if field_name not in storable:
            raise store.DecodeError
        if not type(storable[field_name]) == expected_type:
            raise DecodeError
    return Dude(*itemgetter(*slots)(storable))


dude_schema = Schema(
    name="dude", fields=dude_fields, decode=decode_dude, encode=encode_dude,
)


store_implementations = [DictStore]


@pytest.fixture(params=store_implementations)
def store(request: Any) -> Store:
    return request.param(dude_schema)


harry = Dude("Harry", 11, True)
moomin_Troll = Dude("Moomin", 15, False)
gandalf = Dude("Gandalf The Grey", 5000, True)


@pytest.mark.asyncio
async def test_store_get_set(store: Store[Dude]) -> None:
    harry_key = await store.set(harry)
    assert harry == await store.get(harry_key)
