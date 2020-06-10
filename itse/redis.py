import random
import string

from . import storage


# import typing
#
# import aredis
#
#
# class Connection:
#     client = aredis.StrictRedis(host="127.0.0.1", port=6379, db=0)
#
#
def randomString(stringLength: int = 8) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))

A = TypeVar("A")


class RedisStore(Storage[A]):
    def __init__(self, client: typing.Any, schema: ):
        self.client = client
        self.schema

    def items(self):
        ...
