import typing, datetime
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

class Location(BaseModel):
    latitude: float
    longitude: float

# write a model for food orders
class Order(Document):
    # each order will have a list of items
    items: typing.List[PydanticObjectId]
    # and a total price
    total_price: float
    # the user who made the order
    user_id: typing.Text
    # and the date and time
    date: datetime.datetime
    # and the status of the order
    status: typing.Literal[
        "pending", "accepted", "rejected", "on-the-way", "delivered"
    ] = "pending"
    
    location: Location
    
