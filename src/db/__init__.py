import os
import typing

import motor.motor_asyncio
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

client = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv("MONGO_DB_URI"), uuidRepresentation="standard"
)
db = client[os.getenv("DB_NAME")]


class User(BeanieBaseUser[PydanticObjectId]):
    order_ids: typing.List[PydanticObjectId] = []


async def get_user_db():
    yield BeanieUserDatabase(User)
