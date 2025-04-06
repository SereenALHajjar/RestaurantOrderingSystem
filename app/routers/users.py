from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from app.database import SessionDep
from app.models import Users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep) -> Users:
    """ take the id and return the user """
    db_user = session.exec(select(Users).where(Users.id == user_id)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="No such user")
    return db_user


@router.post("/signup")
async def signup(user: Users, session: SessionDep) -> Users:
    existing_user = session.exec(
        select(Users).where(Users.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


class UserLogin(BaseModel):
    email: str
    password: str

# TODO: store the hashed password and make auth
# TODO: edit the user info


@router.post("/login")
async def login(user: UserLogin, session: SessionDep):
    db_user = session.exec(select(Users).where(
        user.email == Users.email)).first()
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="Invalid email or password")
    if db_user.password != user.password:
        raise HTTPException(
            status_code=400, detail="Invalid email or password")
    return {"message": "Login successful", "user": db_user}
