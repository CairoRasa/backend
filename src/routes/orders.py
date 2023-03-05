from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends
from db import User
import typing
from db.FoodItem import FoodItem
from schemas import OrderRequest
from users import current_active_user
from db.Order import Order as OrderDb

router = APIRouter(prefix="/users/orders", tags=["users_orders"])

@router.get("/")
async def get_orders(user: User = Depends(current_active_user)):
    res = OrderDb.find(OrderDb.user_id == typing.Text(user.id))
    return await res.to_list()

# new route to make a new order for a user
@router.post("/")
async def post_order(order: OrderRequest, user: User = Depends(current_active_user)):
    price = 0
    items = []
    for item in order.item_ids:
        f_item = await FoodItem.find_one(FoodItem.id == ObjectId(item))
        if not f_item:
            return {"message": f"Item {item} not found"}
        price += f_item.price
        items.append(f_item.id)
        
    order_q = OrderDb(
        user_id=typing.Text(user.id),
        items=items,
        status="pending",
        total_price=price,
        location=order.location,
        date=datetime.now()
    )
    order_save_res = await OrderDb(**order_q.dict()).save()
    if order_save_res is None:
        return {"message": "Error placing order"}
    # print(order)
    user.order_ids.append(order_save_res.id) # type: ignore
    # print(user)
    usr_res = await user.save()
    return {
        "order": order_save_res.dict(),
        "message": "Order placed successfully",
        "user": usr_res.id
    }