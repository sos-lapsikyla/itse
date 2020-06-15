from typing import Optional, Protocol

from pydantic import BaseModel

from . import storage


class User(Protocol):
    login_name: str
    password_hash: str
    email: Optional[str]


class UserModel(BaseModel, User)
    login_name: str
    password_hash: str
    email: Optional[str] = None


def decode(storedData: storage.Storable) -> User:
    return User(**storedData)


def encode(user: User) -> storage.Storable:
    return user.dict()


UserSchema = storage.Schema(
    name="user",
    fields={
        "login_name": storage.Field(
            kind="StrKind", required=True, unique=True
        ),
        "password_hash": storage.Field(
            kind="StrKind", required=True, unique=False
        ),
        "email": storage.Field(kind="StrKind", required=False, unique=True),
    },
    decode=decode,
    encode=encode,
)
