from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models import Restaurants
from app.database import SessionDep

router = APIRouter(prefix="/restaurants" , tags=["restaurants"])

@router.get("/get-restaurants")
async def get_restaurants(session:SessionDep):
    return session.exec(select(Restaurants)).all()


@router.get("get-restaurant/{user_id}")
async def get_user(restaurant_id : int , session:SessionDep)->Restaurants:
    """ take the id and return the user """
    db_restaurant = session.exec(select(Restaurants).where(Restaurants.id == restaurant_id)).first()
    if db_restaurant is None:
        raise HTTPException(status_code=404 , detail="No such Restaurant")
    return db_restaurant
    
@router.post("/add-restaurant")
async def add_restaurant(restaurant : Restaurants , session:SessionDep) -> Restaurants:
    existing_restaurant = session.exec(select(Restaurants).where(Restaurants.email == restaurant.email)).first()
    if existing_restaurant:
        raise HTTPException(status_code=400 , detail="Restaurant with this email already exist")
    session.add(restaurant) 
    session.commit() 
    session.refresh(restaurant)
    return restaurant