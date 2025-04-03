# place an order
# get order status
# change order status
# get specific order

import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from app.database import SessionDep
from app.models import Orders, Restaurants, Users

router = APIRouter(prefix="/orders", tags=["orders"])


class Order(BaseModel):
    user_id: int
    restaurant_id: int

@router.get("/status/{order_id}")
async def get_status(order_id:int , session:SessionDep):
    existing_order = session.exec(select(Orders).where(Orders.id == order_id)).first()
    if existing_order is None:
        raise HTTPException(status_code=404 , detail="No such order")
    return {"status":existing_order.status}

@router.post("/add")
async def add_order(order: Order, session: SessionDep):
    restaurant = session.exec(select(Restaurants).where(
        Restaurants.id == order.restaurant_id)).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    user = session.exec(select(Users).where(Users.id == order.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_order = Orders(
        restaurant_id=order.restaurant_id,
        user_id=order.user_id,
        date=datetime.datetime.now(),
        status="pending"
    )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order


@router.patch("/")
async def change_status(order_id:int, new_status: str, session:SessionDep):
    existing_order = session.get(Orders , order_id)
    if not existing_order:
        raise HTTPException(status_code=404 , detail="No such order")
    existing_order.status = new_status
    session.commit()
    session.refresh(existing_order)  
    return {"message": "Order status updated", "order": existing_order}