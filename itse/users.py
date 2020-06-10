from typing import Optional

from pydantic import BaseModel

from .storage import Field, Schema, Storable, Storage


class User(BaseModel):
    login_name: str
    password_hash: str
    email: Optional[str] = None


def decode(storedData: Storable) -> User:
    return User(**storedData)


UserSchema = Schema(
    name="user",
    fields={
        "login_name": Field(kind="StrKind", required=True, unique=True),
        "password_hash": Field(kind="StrKind", required=True, unique=False),
        "email": Field(kind="StrKind", required=False, unique=True),
    },
    decode=decode,
)


# class UserStorage(Storage[User]):
#     pass
