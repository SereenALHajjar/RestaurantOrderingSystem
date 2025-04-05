from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from app.database import SessionDep
from app.models import Order_Details, Orders, Recipes


router = APIRouter(prefix="/orders/details", tags=["order details"])

@router.get("/{order_id}")
def get_order_details(order_id : int , session:SessionDep):
    existing_order = session.exec(select(Order_Details).where(Order_Details.order_id == order_id)).all() ;
    if not existing_order:
        raise HTTPException(status_code=404 , detail="No such order")
    return existing_order 

@router.post("/")
def add_order_details(order_details : Order_Details , session:SessionDep):
    order = session.exec(select(Orders).where(
        Orders.id == order_details.order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    recipe = session.exec(select(Recipes).where(Recipes.id == order_details.recipe_id)).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.add(order_details) 
    session.commit() 
    session.refresh(order_details)
    return order_details

