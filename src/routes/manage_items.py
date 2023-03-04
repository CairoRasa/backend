from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from deps import superuser_authenticated_route
import schemas, db.FoodItem


router = APIRouter(
    prefix="/manage/items",
    tags=["manage_items"],
    dependencies=[Depends(superuser_authenticated_route)],
)


@router.post("/")
async def post_item(item: schemas.FoodItem):
    return await db.FoodItem.FoodItem(**item.dict()).save()


@router.get("/all")
async def get_items():
    res = db.FoodItem.FoodItem.find({})
    return await res.to_list()


@router.patch("/{item_id}")
async def patch_item(item_id: str, item: schemas.FoodItem):
    existing = await db.FoodItem.FoodItem.find_one({"_id": ObjectId(item_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    return await existing.set(
        db.FoodItem.FoodItem(
            name=item.name,
            description=item.description,
            price=item.price,
            image=item.image,
            category=item.category,
            tags=item.tags,
        ).dict()
    )


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    existing = await db.FoodItem.FoodItem.find_one({"_id": ObjectId(item_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        await existing.delete()
    except:
        raise HTTPException(status_code=500, detail="Error deleting item")

    return {"message": "Item deleted successfully"}
