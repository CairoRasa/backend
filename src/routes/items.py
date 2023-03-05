from bson import ObjectId
from fastapi import APIRouter
from db.FoodItem import FoodItem

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def get_items():
    res = FoodItem.find({})
    item_list = await res.to_list()
    for item in item_list:
        delattr(item, "description")
        
    return item_list


@router.get("/{item_id}")
async def get_item(item_id: str):
    return await FoodItem.find_one({"_id": ObjectId(item_id)})