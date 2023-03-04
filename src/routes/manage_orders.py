from fastapi import APIRouter, Depends
from deps import superuser_authenticated_route
from db.Order import Order as OrderDb


router = APIRouter(
    prefix="/manage/orders",
    tags=["manage_orders"],
    dependencies=[Depends(superuser_authenticated_route)],
)


