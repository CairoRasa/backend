from beanie import Document
import typing

class FoodItem(Document):
    name: str
    description: str
    price: float
    image: str
    category: str
    tags: typing.List[str]