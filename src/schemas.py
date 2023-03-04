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
    items: typing.List[FoodItem]
    # and a total price
    total_price: float
    # the user who made the order
    user_id: typing.Text
    # and the status of the order
    # status: typing.Literal[
    #     "pending", "accepted", "rejected", "on-the-way", "delivered"
    # ] = "pending"
    
    location: Location
    