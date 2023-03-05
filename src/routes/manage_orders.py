from bson import ObjectId
from fastapi import APIRouter, Depends
from deps import superuser_authenticated_route
from db.Order import Order as OrderDb
import typing


router = APIRouter(
    prefix="/manage/orders",
    tags=["manage_orders"],
    dependencies=[Depends(superuser_authenticated_route)],
)



@router.patch("/{order_id}")
async def patch_order(
    order_id: str,
    status: typing.Literal[
        "pending", "accepted", "rejected", "on-the-way", "delivered"
    ],
):
    # find the order
    order = await OrderDb.find_one(OrderDb.id == ObjectId(order_id))
    if not order:
        return {"message": "Order not found"}
    # update the status
    order.status = status
    # save the order
    order_save_res = await order.save()
    if order_save_res is None:
        return {"message": "Error updating order"}
    return {"message": "Order updated successfully", "order": order_save_res.dict()}
