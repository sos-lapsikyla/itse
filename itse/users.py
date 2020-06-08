from typing import NamedTuple, Optional

from .storage import Field, Schema


class User(NamedTuple):
    login_name: str
    password_hash: str
    email: Optional[str]


UserSchema = Schema(
    name="User",
    fields={
        "login_name": Field(kind="StrKind", required=True, unique=True),
        "password_hash": Field(kind="StrKind", required=True, unique=False),
        "email": Field(kind="StrKind", required=False, unique=True),
    },
)
