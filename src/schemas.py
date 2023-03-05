from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import BaseModel
import typing

from db.Order import Location

class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

class FoodItem(BaseModel):
    name: str
    description: str
    price: float
    image: str
    category: str
    tags: typing.List[str]
    
    
class OrderRequest(BaseModel):
    # each order will have a list of items
    item_ids: typing.List[typing.Text]
    location: Location
    