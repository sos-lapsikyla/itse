from typing import Optional, Protocol

from pydantic import BaseModel

from . import store


class User(Protocol):
    login_name: str
    password_hash: str
    email: Optional[str]


class UserModel(BaseModel, User):
    login_name: str
    password_hash: str
    email: Optional[str] = None


def decode(storedData: store.Storable) -> User:
    return UserModel(**storedData)


def encode(user: User) -> store.Storable:
    return user.__dict__


UserSchema = store.Schema(
    name="user",
    fields={
        "login_name": store.Field(kind="StrKind", required=True, unique=True),
        "password_hash": store.Field(
            kind="StrKind", required=True, unique=False
        ),
        "email": store.Field(kind="StrKind", required=False, unique=True),
    },
    decode=decode,
    encode=encode,
)
