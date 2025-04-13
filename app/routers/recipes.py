import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlmodel import select
from app.database import SessionDep
from app.models import Recipes, Users

router = APIRouter(prefix="/recipes", tags=["recipes"])

# get all recipe for specific restaurant DONE
# get specific recipe DONE
# add recipe DONE
# TODO: edit prices , name , description , photo , category 
# TODO: delete recipe 


@router.get('/')
async def get_all_recipes(session: SessionDep):
    return session.exec(select(Recipes)).all()


@router.get('/{recipe_id}')
async def get_specific_recipe(recipe_id: int, session: SessionDep):
    existing_recipe = session.exec(
        select(Recipes).where(Recipes.id == recipe_id)).first()
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="No such recipe")
    return existing_recipe

@router.get('/get-photo/{recipe_id}')
async def get_specific_recipe_photo(recipe_id: int, session: SessionDep):
    existing_recipe = session.exec(
        select(Recipes).where(Recipes.id == recipe_id)
    ).first()

    if not existing_recipe:
        raise HTTPException(status_code=404, detail="No such recipe")

    if not existing_recipe.photo:
        raise HTTPException(status_code=404, detail="No photo for this recipe")

    file_path =  existing_recipe.photo


    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image file as a response
    return FileResponse(file_path)

@router.post('/')
async def add_recipe(
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category: str = Form(None),
    restaurant_id: int = Form(...),
    photo: UploadFile|None = File(None),
):
    
    existing_recipe = session.exec(
        select(Recipes).where(
            (Recipes.name == name) &
            (Recipes.restaurant_id == restaurant_id)
        )
    ).first()

    if existing_recipe:
        raise HTTPException(status_code=400, detail="Recipe already exists")
    new_recipe = None 
    if photo:
        file_ext = photo.filename.split(".")[-1]
        filename = f"{uuid4()}.{file_ext}"
        file_path = os.path.join("app" , "static", "uploads", filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    # photo_url = f"C:\\Workspace\\backend\\ResturantOrderingSystesm\\app\\static\\uploads/{filename}" 
        new_recipe = Recipes(
            name=name,
            description=description,
            price=price,
            category=category,
            restaurant_id=restaurant_id,
            photo=file_path
        )
    else:
        new_recipe = Recipes(
            name=name,
            description=description,
            price=price,
            category=category,
            restaurant_id=restaurant_id,
            photo=None
        )
    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)

    return new_recipe
