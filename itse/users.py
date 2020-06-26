from typing import Optional

from pydantic import BaseModel

from .store import Schema


class User(BaseModel):
    login_name: str
    password_hash: str
    email: Optional[str] = None


user_schema = Schema("user", ["name", "email"], User)
