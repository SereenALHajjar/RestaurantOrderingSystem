from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from app.database import SessionDep
from app.models import Recipes, Users

router = APIRouter(prefix="/recipes", tags=["recipes"])

# get all recipe for specific restaurant
# get specific recipe
# add recipe
# edit prices , name , description , photo , category
# delete recipe


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


@router.post('/')
async def add_recipe(recipe: Recipes, session: SessionDep):
    existing_recipe = session.exec(
        select(Recipes).where(
            (Recipes.name == recipe.name) & (
                Recipes.restaurant_id == recipe.restaurant_id)
        )
    ).first()

    if existing_recipe:
        raise HTTPException(
            status_code=400, detail="Recipe with this name already exists for this restaurant")
    session.add(recipe)
    session.commit()
    session.refresh(recipe)

    return {"message": "Recipe added successfully", "recipe": recipe}
