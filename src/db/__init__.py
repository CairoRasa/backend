import motor.motor_asyncio
import os, typing
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client[os.getenv("DB_NAME")]


class User(BeanieBaseUser[PydanticObjectId]):
    order_ids: typing.List[PydanticObjectId] = []


async def get_user_db():
    yield BeanieUserDatabase(User)