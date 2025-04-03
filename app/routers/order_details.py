from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from app.database import SessionDep
from app.models import Users

# add menu

router = APIRouter(prefix="/menus", tags=["order details"])


