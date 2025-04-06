from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import create_db_and_tables
from app.routers import order_details, orders, recipes, restaurants, users

app = FastAPI()


create_db_and_tables()
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(orders.router)
app.include_router(order_details.router)
app.include_router(recipes.router)
app.mount("/uploads", StaticFiles(directory="app/static/uploads"), name="uploads")

