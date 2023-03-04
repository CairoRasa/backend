from fastapi import APIRouter, Depends
from db import User
import typing
from schemas import OrderRequest
from users import current_active_user
from db.Order import Order as OrderDb

router = APIRouter(prefix="/users/orders", tags=["users_orders"])

@router.get("/")
async def get_orders(user: User = Depends(current_active_user)):
    return await OrderDb.find(OrderDb.user_id == typing.Text(user.id)).to_list()

# new route to make a new order for a user
@router.post("/")
async def post_order(order: OrderRequest, user: User = Depends(current_active_user)):
    price = sum(item.price for item in order.items)
    order = OrderDb(
        user_id=typing.Text(user.id),
        items=order.items,
        status="pending",
        total_price=price,
        location=order.location
    )
    order_save_res = await OrderDb(**order.dict()).save()
    # print(order)
    user.order_ids.append(order_save_res.id)
    # print(user)
    usr_res = await user.save()
    return {
        "order": order_save_res.dict(),
        "message": "Order placed successfully",
        "user": usr_res.dict()
    }